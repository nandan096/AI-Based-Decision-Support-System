import pandas as pd

# Standard agricultural transport freight rate in Karnataka (₹2.0 per quintal per km)
DEFAULT_TRANSPORT_RATE_PER_KM = 2.0

# Actual road distances (km) from Bengaluru-Ramanagara production centroid 
# across all 41 monitored Karnataka APMC markets
MARKET_DISTANCES_KM = {
    # South Karnataka / Centroid Belt
    "Ramanagara": 15,
    "Channapatna": 25,
    "Bangalore": 35,
    "Maddur": 42,
    "Mandya": 62,
    "Doddaballa Pur": 72,
    "Malur": 82,
    "Tumkur": 88,
    "Chickballapur": 95,
    "Kolar": 102,
    "Mysore": 110,
    "Chintamani": 115,
    "Channarayapatna": 122,
    "Madhugiri": 130,
    "Nanjangud": 138,
    "Tiptur": 155,
    "Hassan": 165,
    "Arsikere": 185,
    # Central Karnataka
    "Chitradurga": 218,
    "Challakere": 238,
    "Davangere": 265,
    "Bhadravati": 278,
    "Shimoga": 295,
    "Harihar": 300,
    # North Karnataka & Hyderabad-Karnataka Belt
    "Bellary": 320,
    "Hospet": 340,
    "Sagar": 370,
    "Koppal": 375,
    "Gangavathi": 385,
    "Sindhanur": 405,
    "Hubli (Amaragol)": 415,
    "Dharwar": 432,
    "Raichur": 435,
    "Bailhongal": 475,
    "Bagalkot": 482,
    "Belgaum": 505,
    "Yadgir": 510,
    "Bijapur": 525,
    "Jamkhandi": 542,
    "Gulbarga": 575,
    "Bidar": 670,
}

# Case-insensitive and trimmed lookup dictionary to prevent string matching issues
NORMALIZED_DISTANCES = {k.strip().lower(): v for k, v in MARKET_DISTANCES_KM.items()}

# State median highway distance used only if an unmapped mandi is encountered
STATE_MEDIAN_DISTANCE_KM = 265


def get_best_market_analysis(
    df, crop, transport_rate=DEFAULT_TRANSPORT_RATE_PER_KM, top_n=10
):
    """
    Ranks mandis by Net Realized Price (NRP = Modal Price - Freight Tariff).
    Uses true physical centroid highway distances for all 41 APMC markets.
    """
    crop_df = df[df['Commodity'] == crop].copy()

    # Accommodate both 'Market Name' and 'Market' column naming
    market_col = 'Market Name' if 'Market Name' in crop_df.columns else 'Market'

    # Retrieve the latest market price record for each APMC market
    latest = (
        crop_df.sort_values('Price Date')
        .groupby(market_col)
        .last()
        .reset_index()
    )

    # 1. Clean market names and map to real highway distances
    def resolve_distance(market_name):
        cleaned = str(market_name).strip().lower()
        if cleaned in NORMALIZED_DISTANCES:
            return NORMALIZED_DISTANCES[cleaned]
        print(f"[Warning] Unmapped Mandi: '{market_name}'. Using state median {STATE_MEDIAN_DISTANCE_KM} km.")
        return STATE_MEDIAN_DISTANCE_KM

    latest['Distance (km)'] = latest[market_col].apply(resolve_distance)

    # 2. Compute freight deduction: c * d_m (Rs. 2.0/km/qtl)
    latest['Transport Cost (₹/Qtl)'] = (
        latest['Distance (km)'] * transport_rate
    ).round(2)

    # 3. Compute Net Realized Price: NRP = P_m - (c * d_m)
    latest['Net Price (₹/Qtl)'] = (
        latest['Modal_Price'] - latest['Transport Cost (₹/Qtl)']
    ).round(2)

    # 4. Rank by take-home Net Realized Price
    latest = latest.sort_values('Net Price (₹/Qtl)', ascending=False).reset_index(
        drop=True
    )

    best_market = latest.iloc[0][market_col]
    best_net_price = latest.iloc[0]['Net Price (₹/Qtl)']

    # 5. Format display table
    market_table = latest[[
        market_col,
        'Distance (km)',
        'Modal_Price',
        'Transport Cost (₹/Qtl)',
        'Net Price (₹/Qtl)',
    ]].head(top_n)

    market_table.columns = [
        'Market',
        'Est. Distance (km)',
        'Gross Price (₹/Qtl)',
        'Transport Cost (₹/Qtl)',
        'Net Realized Price (₹/Qtl)',
    ]

    return best_market, best_net_price, market_table