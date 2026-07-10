import streamlit as st
import pandas as pd

from predict import predict_price
from market import get_best_market_analysis

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="AI-Based Agricultural Decision Support System",
    page_icon="🌾",
    layout="wide"
)

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

df = pd.read_csv("data/Processed Data/Karnataka_Processed.csv")

df["Price Date"] = pd.to_datetime(
    df["Price Date"],
    format="%d/%m/%Y"
)

# ----------------------------------------------------
# Title
# ----------------------------------------------------

st.title("🌾 AI-Based Agricultural Decision Support System")
st.subheader("Smart Agricultural Marketing using Artificial Intelligence")

st.markdown("---")

# ====================================================
# About Project + Farmer Inputs — SAME ROW
# ====================================================

about_col, input_col = st.columns([2, 1])

with about_col:

    st.markdown("### 📌 About the Project")

    st.write("""
    This AI-Based Decision Support System assists farmers by analyzing 
    historical agricultural market prices and providing intelligent recommendations.
    """)

    st.markdown("**Key Features**")

    st.write("""
    - 🌾 Predicts crop prices using Machine Learning
    - 🧠 Automatically selects the best-performing model for each crop
    - 📈 Estimates future profit
    - 💰 Provides Sell / Wait recommendations
    - 🏪 Recommends the best market for selling
    - 📊 Uses historical market data instead of fixed sample values
    """)

with input_col:

    st.subheader("👨‍🌾 Farmer Inputs")

    crop = st.selectbox(
        "Select Crop",
        ["Onion", "Tomato", "Potato"]
    )

    quantity = st.number_input(
        "Quantity (Quintals)",
        min_value=1,
        value=100
    )

    production_cost = st.number_input(
        "Production Cost (₹ / Quintal)",
        min_value=0,
        value=1800
    )

    predict = st.button(
        "🚀 Predict",
        use_container_width=True
    )

st.markdown("---")

# ====================================================
# Results Section
# ====================================================

if predict:

    crop_df = df[df["Commodity"] == crop].copy()

    crop_df = (
        crop_df
        .groupby("Price Date")["Modal_Price"]
        .mean()
        .reset_index()
    )

    crop_df = crop_df.sort_values("Price Date")

    sample_prices = crop_df["Modal_Price"].tail(30).tolist()

    if len(sample_prices) < 30:
        st.error("Not enough historical data available.")
        st.stop()

    predicted_price = predict_price(sample_prices, crop)

    today_price = sample_prices[-1]

    difference = predicted_price - today_price

    percentage = (difference / today_price) * 100

    if difference > 0:
        recommendation = "WAIT"
        reason = "Price is expected to increase."
    else:
        recommendation = "SELL NOW"
        reason = "Price is expected to decrease."

    # ====================================================
    # Prediction Result
    # ====================================================

    st.subheader("📊 Prediction Result")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Today's Price", f"₹{today_price:.2f}")
    c2.metric("Predicted Price", f"₹{predicted_price:.2f}")
    c3.metric("Expected Change", f"₹{difference:.2f}")
    c4.metric("% Change", f"{percentage:.2f}%")

    if recommendation == "WAIT":
        st.success("✅ Recommendation : WAIT")
    else:
        st.error("❌ Recommendation : SELL NOW")

    st.info(reason)

    st.markdown("---")

    # ====================================================
    # Profit Analysis
    # ====================================================

    today_revenue = today_price * quantity
    tomorrow_revenue = predicted_price * quantity

    today_profit = (today_price - production_cost) * quantity
    tomorrow_profit = (predicted_price - production_cost) * quantity

    profit_difference = tomorrow_profit - today_profit

    st.subheader("💰 Farmer Profit Analysis")

    p1, p2 = st.columns(2)

    with p1:
        st.metric("Today's Revenue", f"₹{today_revenue:,.2f}")
        st.metric("Today's Profit", f"₹{today_profit:,.2f}")

    with p2:
        st.metric("Predicted Revenue", f"₹{tomorrow_revenue:,.2f}")
        st.metric("Predicted Profit", f"₹{tomorrow_profit:,.2f}")

    if profit_difference > 0:
        st.success(f"💰 Expected Extra Profit : ₹{profit_difference:,.2f}")
    else:
        st.error(f"📉 Expected Loss : ₹{abs(profit_difference):,.2f}")

    st.markdown("---")

    # ====================================================
    # Best Market
    # ====================================================

    best_market, best_price, market_table = get_best_market_analysis(df, crop)

    st.subheader("🏪 Recommended Market")

    m1, m2 = st.columns(2)

    with m1:
        st.metric("🏆 Best Market", best_market)

    with m2:
        st.metric("Latest Market Price", f"₹{best_price:.2f}")

    st.info("Highest latest market price among Karnataka markets.")

    st.markdown("---")

    # ====================================================
    # Market Comparison
    # ====================================================

    st.subheader("📊 Top 10 Market Comparison")

    st.dataframe(
        market_table,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("👈 Select your crop and inputs above, then click **🚀 Predict**")

st.markdown("---")

st.caption(
    "AI-Based Decision Support System | Built using Streamlit, TensorFlow, Scikit-learn and Python"
)   

