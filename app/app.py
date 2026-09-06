import pandas as pd
import streamlit as st
from market import get_best_market_analysis
from predict import predict_price

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="AI-Based Agricultural Decision Support System",
    page_icon="🌾",
    layout="wide",
)

# ----------------------------------------------------
# Economic & Holding Cost Parameters (per 24h horizon)
# ----------------------------------------------------
# Tomato: High transpirational weight loss & perishable decay
# Potato: Cold storage handling & anti-sprouting buffer
# Onion: Bagging, dry-shed ventilation, and moisture shrinkage
HOLDING_COSTS = {
    "Tomato": 18.0,  # ₹18/qtl/day
    "Potato": 6.0,   # ₹6/qtl/day
    "Onion": 4.0     # ₹4/qtl/day
}
THETA_BUFFER = 50.0  # Risk buffer threshold (₹/quintal)

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

df = pd.read_csv("data/Processed Data/Karnataka_Processed.csv")
df["Price Date"] = pd.to_datetime(df["Price Date"], format="%d/%m/%Y")

# ----------------------------------------------------
# Title & Header
# ----------------------------------------------------

st.title("🌾 AI-Based Agricultural Decision Support System")
st.subheader("Smart Agricultural Marketing using Artificial Intelligence")

st.markdown("---")

# ====================================================
# About Project + Farmer Inputs
# ====================================================

about_col, input_col = st.columns([2, 1])

with about_col:
    st.markdown("### 📌 About the Project")
    st.write(
        """
        This AI-Based Decision Support System assists farmers by analyzing 
        historical agricultural market prices and providing intelligent recommendations.
        """
    )

    st.markdown("**Key Features**")
    st.write(
        """
        - 🌾 Predicts crop prices using Machine Learning
        - 🧠 Uses the best-performing model selected for each crop
        - 📈 Estimates future profit and net returns after storage/spoilage deduction
        - 💰 Provides Sell / Wait directives based on the Net Holding Return (NHR) engine
        - 🏪 Recommends the best market accounting for net transport freight
        - 📊 Uses historical market transaction data across Karnataka APMCs
        """
    )

with input_col:
    st.subheader("👨‍🌾 Farmer Inputs")

    crop = st.selectbox("Select Crop", ["Onion", "Tomato", "Potato"])

    quantity = st.number_input("Quantity (Quintals)", min_value=1, value=100)

    default_costs = {"Onion": 1500, "Tomato": 800, "Potato": 1000}

    production_cost = st.number_input(
        "Production Cost (₹ / Quintal)",
        min_value=0,
        value=default_costs.get(crop, 1000),
        step=50,
    )

    predict = st.button("🚀 Predict", use_container_width=True)

st.markdown("---")

# ====================================================
# Results Section
# ====================================================

if predict:
    crop_df = df[df["Commodity"] == crop].copy()
    crop_df = crop_df.groupby("Price Date")["Modal_Price"].mean().reset_index()
    crop_df = crop_df.sort_values("Price Date")

    sample_prices = crop_df["Modal_Price"].tail(30).tolist()

    if len(sample_prices) < 30:
        st.error("Not enough historical data available.")
        st.stop()

    latest_month = crop_df["Price Date"].iloc[-1].month
    predicted_price = predict_price(sample_prices, crop, month=latest_month)
    today_price = sample_prices[-1]

    # ----------------------------------------------------
    # True Net Holding Return (NHR) Engine
    # NHR = (P_hat_{t+1} - P_t) - (C_storage + C_spoilage)
    # Decision = WAIT if NHR >= THETA_BUFFER else SELL NOW
    # ----------------------------------------------------
    storage_and_spoilage_cost = HOLDING_COSTS.get(crop, 5.0)
    gross_price_change = predicted_price - today_price
    percentage_change = (gross_price_change / today_price) * 100

    nhr = gross_price_change - storage_and_spoilage_cost

    if nhr >= THETA_BUFFER:
        recommendation = "WAIT"
        rec_status = "success"
        reason = (
            f"Projected price appreciation (+₹{gross_price_change:.2f}/Qtl) "
            f"exceeds holding & spoilage costs (₹{storage_and_spoilage_cost:.2f}/Qtl) "
            f"and clears the ₹{THETA_BUFFER:.2f}/Qtl risk buffer threshold "
            f"(Net Holding Return: +₹{nhr:.2f}/Qtl)."
        )
    else:
        recommendation = "SELL NOW"
        rec_status = "error"
        if gross_price_change > 0:
            reason = (
                f"Gross price rise (+₹{gross_price_change:.2f}/Qtl) is insufficient. "
                f"After deducting daily holding & spoilage degradation (₹{storage_and_spoilage_cost:.2f}/Qtl), "
                f"the Net Holding Return is only ₹{nhr:.2f}/Qtl, failing to satisfy "
                f"the ₹{THETA_BUFFER:.2f}/Qtl risk buffer."
            )
        else:
            reason = (
                f"Price is projected to decline or remain stagnant (Gross Change: ₹{gross_price_change:.2f}/Qtl). "
                f"Holding carries uncompensated market and spoilage risk."
            )

    # ====================================================
    # Prediction Result
    # ====================================================

    st.subheader("📊 Prediction & Decision Support Output")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Prevailing Modal Price", f"₹{today_price:.2f}")
    c2.metric("Predicted 24h Price", f"₹{predicted_price:.2f}")
    c3.metric("Gross Change", f"₹{gross_price_change:.2f} ({percentage_change:.2f}%)")
    c4.metric(
        "Net Holding Return (NHR)",
        f"₹{nhr:.2f} / Qtl",
        help=f"Gross change minus daily holding & spoilage cost (₹{storage_and_spoilage_cost:.2f}/Qtl)",
    )

    if recommendation == "WAIT":
        st.success(f"✅ Directive: **{recommendation}**")
    else:
        st.error(f"❌ Directive: **{recommendation}**")

    st.info(f"💡 **Economic Justification:** {reason}")

    st.markdown("---")

    # ====================================================
    # Profit Analysis
    # ====================================================

    today_revenue = today_price * quantity
    today_profit = (today_price - production_cost) * quantity

    total_holding_cost = storage_and_spoilage_cost * quantity
    tomorrow_revenue = predicted_price * quantity
    tomorrow_profit = (predicted_price - production_cost) * quantity - total_holding_cost

    profit_difference = tomorrow_profit - today_profit

    st.subheader("💰 Farmer Profit Analysis (Adjusted for Holding Overheads)")

    p1, p2 = st.columns(2)
    with p1:
        st.metric("Today's Revenue", f"₹{today_revenue:,.2f}")
        st.metric("Today's Net Margin", f"₹{today_profit:,.2f}")

    with p2:
        st.metric("Projected Revenue (Day t+1)", f"₹{tomorrow_revenue:,.2f}")
        st.metric(
            "Projected Net Margin (After Holding)",
            f"₹{tomorrow_profit:,.2f}",
            help=f"Includes deduction of ₹{total_holding_cost:,.2f} storage & spoilage cost.",
        )

    if profit_difference >= (THETA_BUFFER * quantity):
        st.success(
            f"💰 Expected Net Gain if you WAIT: +₹{profit_difference:,.2f} "
            f"(Clears total risk threshold buffer of ₹{THETA_BUFFER * quantity:,.2f})"
        )
    elif profit_difference > 0:
        st.warning(
            f"⚠️ Marginal Gain: +₹{profit_difference:,.2f} "
            f"(Does not clear the minimum risk buffer of ₹{THETA_BUFFER * quantity:,.2f}; selling now recommended)"
        )
    else:
        st.warning(
            f"📉 Opportunity Loss if you WAIT: -₹{abs(profit_difference):,.2f} "
            f"(Sell now to protect realized profit)"
        )

    st.markdown("---")

    # ====================================================
    # Best Market (Net Realized Return)
    # ====================================================

    best_market, best_net_price, market_table = get_best_market_analysis(df, crop)

    st.subheader("🏪 Recommended Market (Net Realized Return)")

    m1, m2 = st.columns(2)
    with m1:
        st.metric("🏆 Best Market", best_market)

    with m2:
        st.metric(
            "Net Take-Home Price",
            f"₹{best_net_price:,.2f} / Qtl",
            help="Market modal price minus estimated transportation freight cost.",
        )

    st.info(
        "💡 **Freight Arbitrage Reality:** Market recommendations factor in **Net Realized Price** "
        "(Modal Price − Transportation Freight) calculated from the Bengaluru/Ramanagara agricultural "
        "production centroid at ₹2.0/km per quintal. This prevents misleading recommendations for distant mandis "
        "with deceptive unadjusted spot prices."
    )

    st.markdown("---")

    # ====================================================
    # Market Comparison Table
    # ====================================================

    st.subheader("📊 Top 10 Market Comparison")

    st.dataframe(market_table, use_container_width=True, hide_index=True)

else:
    st.info("👈 Select your crop and inputs above, then click **🚀 Predict**")

st.markdown("---")

st.caption(
    "AI-Based Decision Support System | Built using Streamlit, Scikit-learn and Python"
)