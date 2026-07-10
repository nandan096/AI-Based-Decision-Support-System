import pandas as pd

def get_best_market_analysis(df, crop, top_n=10):

    crop_df = df[
        df["Commodity"] == crop
    ].copy()

    latest = (
        crop_df
        .sort_values("Price Date")
        .groupby("Market Name")
        .last()
        .reset_index()
    )

    latest = latest.sort_values(
        "Modal_Price",
        ascending=False
    ).reset_index(drop=True)

    best_market = latest.iloc[0]["Market Name"]

    best_price = latest.iloc[0]["Modal_Price"]

    market_table = latest[
        ["Market Name","Modal_Price"]
    ].head(top_n)

    market_table.columns = [
        "Market",
        "Latest Price (₹/Quintal)"
    ]

    return best_market, best_price, market_table