# 🌾 AI-Based Decision Support System for Agricultural Price Prediction and Market Recommendation

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-LSTM-FF6F00?style=flat&logo=tensorflow&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-green?style=flat)

An end-to-end Machine Learning and Decision Support System designed to assist smallholder farmers in Karnataka, India. The system forecasts commodity market prices using crop-specific predictive models, computes potential net profits, provides actionable **SELL NOW** or **WAIT** recommendations, and identifies the highest-paying APMC market (mandi) in real time after deducting regional transport freight.

---

## 🌐 Live Application & Source Code

- **Live Interactive Dashboard:** https://ai-based-decision-support-system.streamlit.app/
- **GitHub Repository:** https://github.com/nandan096/AI-Based-Decision-Support-System

---

## 📌 Project Overview

Agricultural commodity prices in India are subject to high volatility caused by weather patterns, localized harvest gluts, and supply chain frictions. Existing market information portals provide only historical or static spot rates, forcing farmers into distressed sales immediately after harvest.

This project bridges that gap by coupling time-series machine learning price predictions with economic decision-support features:

1. **Crop-Specific Model Selection:** Evaluates multiple algorithms per commodity rather than forcing a one-size-fits-all model across differing perishability and storage dynamics.
2. **Economic Decision Engine:** Translates predicted forward prices into actionable sell/wait guidance based on holding costs, perishability risk, and an empirical risk buffer.
3. **Transport-Aware Mandi Recommendation:** Ranks Karnataka APMC markets by Net Realized Price (Modal Price minus freight cost) so farmers do not lose profits traveling to distant markets.

---

## 📊 Dataset & Preprocessing

The system utilizes official market transaction records retrieved from the **AGMARKNET** portal:

- **Raw Records:** 737,392 records across India
- **Regional Focus:** Karnataka state APMC markets (41 mandis)
- **Target Commodities:** Onion, Tomato, Potato
- **Cleaned Dataset:** 12,774 chronological records spanning 24 months (June 2023 – June 2025)
- **Preprocessing Pipeline:** Removal of zero-price records, 99th-percentile outlier filtering, datetime standardization, commodity-wise separation, and chronological 80/20 train/test splitting (zero look-ahead leakage).

---

## 🧠 Experimental Benchmarking & Model Selection

Commodities exhibit distinct economic profiles (e.g., tomato is highly perishable, while onion and potato feature storage cycles). Models were evaluated on chronological 80/20 test partitions against Mean Absolute Error (MAE), Root Mean Square Error (RMSE), Mean Absolute Percentage Error (MAPE), and the Coefficient of Determination ($R^2$).

### Model Benchmark Summary

| Commodity  | Evaluated Model       | RMSE (₹/Qtl) | MAE (₹/Qtl) | MAPE (%)   | $R^2$ Score | Selection Status           |
| :--------- | :-------------------- | :----------- | :---------- | :--------- | :---------- | :------------------------- |
| **Onion**  | **Linear Regression** | **330.82**   | **199.63**  | **9.38%**  | **0.8587**  | **Selected (OLS Optimal)** |
| Onion      | Naive (Persistence)   | 331.06       | 176.42      | 8.73%      | 0.8584      | Baseline                   |
| Onion      | Random Forest         | 369.36       | 222.56      | 10.77%     | 0.8238      | Baseline                   |
| Onion      | Gradient Boosting     | 382.63       | 228.70      | 10.75%     | 0.8109      | Baseline                   |
| **Tomato** | **Linear Regression** | **289.57**   | **192.05**  | **18.94%** | **0.3705**  | **Selected (Deployed)**    |
| Tomato     | Gradient Boosting     | 301.26       | 216.52      | 20.40%     | 0.3186      | Baseline                   |
| Tomato     | Naive (Persistence)   | 313.47       | 206.13      | 20.32%     | 0.2623      | Baseline                   |
| Tomato     | Random Forest         | 343.44       | 238.56      | 22.17%     | 0.1145      | Baseline                   |
| **Potato** | **Gradient Boosting** | **369.23**   | **264.97**  | **13.34%** | **0.3050**  | **Selected (Deployed)**    |
| Potato     | Linear Regression     | 385.22       | 253.30      | 12.88%     | 0.2436      | Baseline                   |
| Potato     | Random Forest         | 382.12       | 276.56      | 13.72%     | 0.2557      | Baseline                   |
| Potato     | Naive (Persistence)   | 393.93       | 269.51      | 14.28%     | 0.2090      | Baseline                   |

### Comparative Findings

- **Onion (Near-Martingale Persistence):** Onion prices exhibit high temporal autocorrelation ($r > 0.92$). The Linear Regression model minimizes squared error loss via OLS, matching persistence performance while accommodating weekly calendar effects.
- **Tomato (Perishable Shock Resilience):** Autoregressive lag features allow Linear Regression to beat the naive baseline decisively ($R^2 = 0.3705$ vs $0.2623$), lowering MAPE from 20.32% to 18.94%.
- **Potato (Non-Linear Storage Cycles):** Non-linear Gradient Boosting captures storage releases better than linear and naive baselines ($R^2 = 0.3050$ vs $0.2090$).

### Hyperparameters & Features

- **Onion (Linear Regression):** Lags 1, 2, 7; 7-day rolling mean; calendar month index.
- **Tomato (Linear Regression):** Lags 1, 2, 3; 3-day rolling mean.
- **Potato (Gradient Boosting Regressor):** `n_estimators=100`, `max_depth=3`, `learning_rate=0.1`, `random_state=42`; Lags 1, 2, 7; 7-day rolling mean; calendar month index.

---

## ⚖️ Decision Support Logic

### 1. Sell / Wait Economic Rule

The decision module converts future price predictions into practical recommendations through a **Net Holding Return (NHR)** rule:

$$\text{NHR} = (\hat{P}_{t+1} - P_t) - (C_{\text{storage}} + C_{\text{spoilage}})$$

Where:

- $\hat{P}_{t+1}$ = Predicted next-day modal price
- $P_t$ = Current APMC modal price
- $C_{\text{storage}}$ = Estimated holding/warehousing cost per quintal
- $C_{\text{spoilage}}$ = Estimated loss rate from commodity quality deterioration

**Threshold Justification ($\theta = ₹50/\text{quintal}$):**

- **WAIT:** Triggered when $\text{NHR} > \theta$. The ₹50/qtl threshold represents an empirical minimum risk buffer margin (equivalent to ~2–4% of median commodity prices). It prevents speculative holding recommendations driven by minor intraday noise or model margin of error.
- **SELL NOW:** Triggered when $\text{NHR} \le \theta$, indicating expected price drops, flat markets, or potential gains that do not compensate for holding risk.

### 2. Mandi Recommendation with Net Realized Freight

To prevent misleading recommendations from distant mandis where freight costs exceed price differences, markets are evaluated on **Net Realized Price**:

$$\text{Net Price} = \text{Modal Price} - (\text{Distance (km)} \times c)$$

**Freight Parameter Justification ($c = ₹2.00/\text{km per quintal}$):**  
In Karnataka rural logistics, smallholders typically pool produce using Light Commercial Vehicles (e.g., Tata Ace / Mahindra Bolero) carrying 15–20 quintals at an average hiring rate of ₹30–₹40/km:

$$\frac{₹35/\text{km}}{17.5\text{ quintals}} \approx ₹2.00/\text{km/quintal}$$

---

## 📁 Project Structure

```text
AI-Based-Decision-Support-System/
│
├── app/
│   ├── app.py                     # Streamlit web interface and dashboard
│   ├── predict.py                 # Feature extraction and multi-model inference
│   └── market.py                  # APMC mandi ranking and freight-adjusted logic
│
├── Models/
│   ├── models/
│   │   ├── onion_lr.pkl           # Selected: Linear Regression (R² = 0.8587)
│   │   ├── tomato_lr.pkl          # Selected: Linear Regression (R² = 0.3705)
│   │   ├── potato_gb.pkl          # Selected: Gradient Boosting (R² = 0.3050)
│   │   └── onion_model.h5         # Evaluated: Deep Learning LSTM Sequence Baseline
│   │
│   └── scalers/
│       ├── onion_scaler.pkl       # Scaler artifact for LSTM sequence input
│       ├── tomato_scaler.pkl      # Scaler artifact for Tomato pipeline
│       └── potato_scaler.pkl      # Scaler artifact for Potato pipeline
│
├── data/
│   ├── Raw Data/
│   │   └── Agriculture_price_dataset.csv     # Raw AGMARKNET dataset
│   └── Processed Data/
│       └── Karnataka_Processed.csv           # Cleaned Karnataka records
│
├── Notebooks/
│   ├── 01_Data_Understanding.ipynb           # Exploratory data analysis
│   ├── 02_Preprocessing.ipynb                # Outlier filtering and date formatting
│   ├── 03_Model_Training.ipynb               # Deep learning LSTM sequence modeling
│   ├── 04_Model_Comparison.ipynb             # ML model benchmarking (LR, RF, GBR)
│   └── 05_Decision_Support_Engine.ipynb      # Decision rule and profit engine testing
│
├── Paper/
│   └── conference-template-a4.docx           # Academic research paper manuscript
│
├── requirements.txt                          # Production Python dependencies
├── runtime.txt                               # Python runtime specification
├── .gitignore
└── README.md
```


---

## ⚙️ Installation & Local Execution

### Prerequisites

- Python 3.11+
- Git

### Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/nandan096/AI-Based-Decision-Support-System.git
cd AI-Based-Decision-Support-System

```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```

3. **Install dependencies:**

```bash
pip install -r requirements.txt

```

4. **Launch the Streamlit application:**

```bash
streamlit run app/app.py

```

---

## 🛠 Tech Stack

- **Language:** Python 3.11
- **Frontend / Deployment:** Streamlit, Streamlit Cloud
- **Machine Learning:** Scikit-learn, Joblib
- **Deep Learning Baseline:** TensorFlow / Keras (LSTM)
- **Data Processing & Analytics:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn

---

## 📄 License

This project is intended for educational and research purposes.

```

```
