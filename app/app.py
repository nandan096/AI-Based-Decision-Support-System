import pandas as pd
from market import get_best_market_analysis
from predict import predict_price
import streamlit as st

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="AI-Based Agricultural Decision Support System",
    page_icon="🌾",
    layout="wide",
)

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

df = pd.read_csv("data/Processed Data/Karnataka_Processed.csv")
df["Price Date"] = pd.to_datetime(df["Price Date"], format="%d/%m/%Y")

# ----------------------------------------------------
# Title
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
  st.write("""
    This AI-Based Decision Support System assists farmers by analyzing 
    historical agricultural market prices and providing intelligent recommendations.
    """)

  st.markdown("**Key Features**")
  st.write("""
    - 🌾 Predicts crop prices using Machine Learning
    - 🧠 Uses the best-performing model selected for each crop
    - 📈 Estimates future profit and potential gain from holding
    - 💰 Provides Sell / Wait recommendations based on expected price movement
    - 🏪 Recommends the best market accounting for net transport freight
    - 📊 Uses historical market transaction data across Karnataka APMCs
    """)

with input_col:
  st.subheader("👨‍🌾 Farmer Inputs")

  crop = st.selectbox("Select Crop", ["Onion", "Tomato", "Potato"])

  quantity = st.number_input("Quantity (Quintals)", min_value=1, value=100)

  # Realistic default cost per crop
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
  # Economic Decision Engine (Threshold theta = Rs. 50/qtl)
  # ----------------------------------------------------
  THETA_BUFFER = 50.0  # Holding risk threshold (₹/Qtl)

  difference = predicted_price - today_price
  percentage = (difference / today_price) * 100

  if difference > THETA_BUFFER:
    recommendation = "WAIT"
    reason = (
        f"Expected price rise of ₹{difference:.2f}/Qtl exceeds the "
        f"₹{THETA_BUFFER:.2f}/Qtl holding-risk threshold."
    )
  else:
    recommendation = "SELL NOW"
    if difference > 0:
      reason = (
          f"Expected gain of ₹{difference:.2f}/Qtl is insufficient to "
          "justify holding the produce after considering storage and price"
          " risk."
      )
    else:
      reason = (
          "Price is projected to decline or remain flat. Selling now is"
          " recommended."
      )

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

  if profit_difference > (THETA_BUFFER * quantity):
    st.success(
        f"💰 Expected Gain if you WAIT: +₹{profit_difference:,.2f} (Exceeds"
        f" holding threshold of ₹{THETA_BUFFER * quantity:,.2f})"
    )
  elif profit_difference > 0:
    st.warning(
        f"⚠️ Nominal Gain: +₹{profit_difference:,.2f} (Does not cover minimum"
        f" risk buffer of ₹{THETA_BUFFER * quantity:,.2f}; selling now"
        " recommended)"
    )
  else:
    st.warning(
        f"📉 Opportunity Loss if you WAIT: -₹{abs(profit_difference):,.2f}"
        " (Sell now to protect profits)"
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
      "💡 **Economic Reality Note:** Market recommendations factor in **Net"
      " Realized Price** (Market Price − Transport Freight) calculated from the"
      " central farming cluster (Bengaluru/Ramanagara hub) at ₹2.0/km per"
      " quintal. This prevents misleading recommendations from mandis that"
      " appear profitable on paper but lose money after freight."
  )

  st.markdown("---")

  # ====================================================
  # Market Comparison
  # ====================================================

  st.subheader("📊 Top 10 Market Comparison")

  st.dataframe(market_table, use_container_width=True, hide_index=True)

else:
  st.info("👈 Select your crop and inputs above, then click **🚀 Predict**")

st.markdown("---")

st.caption(
    "AI-Based Decision Support System | Built using Streamlit, Scikit-learn and"
    " Python"
)