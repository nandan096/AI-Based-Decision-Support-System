import pandas as pd

# Approximate road distances (in km) from central farming hub (Bengaluru / Ramanagara)
# to key Karnataka APMC mandis
MARKET_DISTANCES_KM = {
    'Bangalore': 15,
    'Ramanagara': 45,
    'Doddaballa Pur': 40,
    'Chintamani': 75,
    'Kolar': 70,
    'Tumkur': 70,
    'Mysore': 145,
    'Hospet': 330,
    'Bellary': 310,
    'Hubli (Amaragol)': 410,
    'Belgaum': 505,
    'Dharwar': 425,
    'Shimoga': 280,
    'Hassan': 185,
    'Davangere': 260,
}

# Standard agricultural transport freight rate in Karnataka (~₹2.0 per quintal per km)
DEFAULT_TRANSPORT_RATE_PER_KM = 2.0


def get_best_market_analysis(
    df, crop, transport_rate=DEFAULT_TRANSPORT_RATE_PER_KM, top_n=10
):
  crop_df = df[df['Commodity'] == crop].copy()

  # Get latest price entry for each market
  latest = (
      crop_df.sort_values('Price Date')
      .groupby('Market Name')
      .last()
      .reset_index()
  )

  # 1. Map distance (defaults to 100 km if mandi not explicitly listed)
  latest['Distance (km)'] = latest['Market Name'].apply(
      lambda m: MARKET_DISTANCES_KM.get(m, 100)
  )

  # 2. Compute Transport Cost per quintal
  latest['Transport Cost (₹/Qtl)'] = (
      latest['Distance (km)'] * transport_rate
  ).round(2)

  # 3. Compute Net Realized Price
  latest['Net Price (₹/Qtl)'] = (
      latest['Modal_Price'] - latest['Transport Cost (₹/Qtl)']
  ).round(2)

  # 4. Rank by Net Realized Price (economic reality) instead of raw price
  latest = latest.sort_values('Net Price (₹/Qtl)', ascending=False).reset_index(
      drop=True
  )

  best_market = latest.iloc[0]['Market Name']
  best_net_price = latest.iloc[0]['Net Price (₹/Qtl)']
  best_gross_price = latest.iloc[0]['Modal_Price']

  # Prepare clean display table
  market_table = latest[[
      'Market Name',
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