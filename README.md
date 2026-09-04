# 🌾 AI-Based Decision Support System for Agricultural Price Prediction and Market Recommendation

An end-to-end Machine Learning and Decision Support System designed to assist smallholder farmers in Karnataka, India. The system forecasts commodity market prices using crop-specific predictive models, computes potential net profits, provides actionable **SELL NOW** or **WAIT** recommendations, and identifies the highest-paying APMC market (mandi) in real time.

---

## 🌐 Live Application & Source Code

* **Live Interactive Dashboard:** [https://ai-based-decision-support-system.streamlit.app/](https://ai-based-decision-support-system.streamlit.app/)
* **GitHub Repository:** [https://github.com/nandan096/AI-Based-Decision-Support-System](https://github.com/nandan096/AI-Based-Decision-Support-System)

---

## 📌 Project Overview

Agricultural commodity prices in India are subject to high volatility caused by weather patterns, localized harvest gluts, and supply chain frictions. Existing market information portals provide only historical or static spot rates, forcing farmers into distressed sales immediately after harvest.

This project bridges that gap by coupling time-series machine learning price predictions with economic decision-support features:

1. **Crop-Specific Model Selection:** Evaluates multiple algorithms per commodity rather than forcing a one-size-fits-all model across differing perishability and storage dynamics.


2. **Economic Decision Engine:** Translates predicted forward prices into actionable sell/wait guidance based on holding costs and risk margins.


3. **Mandi Recommendation:** Identifies optimal selling locations across Karnataka APMC markets based on the latest modal prices.



---

## 📊 Dataset & Preprocessing

The system utilizes official market transaction records retrieved from the **AGMARKNET** portal:

* **Raw Records:** 737,392 records across India


* **Regional Focus:** Karnataka state APMC markets (41 mandis)


* **Target Commodities:** Onion, Tomato, Potato


* **Cleaned Dataset:** 12,774 chronological records spanning 24 months (June 2023 – June 2025)


* **Preprocessing Pipeline:** Removal of zero-price records, 99th-percentile outlier filtering, datetime standardization, commodity-wise separation, and chronological 80/20 train/test splitting (zero look-ahead leakage).



---

## 🧠 Experimental Benchmarking & Model Selection

Commodities exhibit distinct economic profiles (e.g., tomato is highly perishable, while onion and potato feature cold-storage cycles). The models were evaluated using chronological test partitions against Mean Absolute Error (MAE), Root Mean Square Error (RMSE), and the Coefficient of Determination ($R^2$).

### Model Benchmark Summary

| Commodity | Evaluated Model | RMSE (₹/Quintal) | MAE (₹/Quintal) | $R^2$ Score | Selection Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Onion** | **Linear Regression** | **330.82** | **199.63** | **0.8587** | **Selected (Fast/Linear)** |
| Onion | Random Forest | 369.36 | 222.56 | 0.8238 | Benchmark Baseline |
| Onion | Gradient Boosting | 382.63 | 228.70 | 0.8109 | Benchmark Baseline |
| Onion | LSTM Network | 443.42 | 289.20 | 0.7199 | Deployed Deep Learning Model |
| **Tomato** | **Linear Regression (Lags 1–3)** | **289.57** | **192.05** | **0.3705** | **Selected** |
| Tomato | Gradient Boosting | 301.26 | 216.52 | 0.3186 | Benchmark Baseline |
| Tomato | Random Forest | 343.44 | 238.56 | 0.1145 | Deployed Baseline Model |
| **Potato** | **Gradient Boosting (Lags 1–7)** | **369.23** | **264.97** | **0.3050** | **Selected** |
| Potato | Random Forest | 382.12 | 276.56 | 0.2557 | Deployed Baseline Model |
| Potato | Linear Regression | 385.22 | 253.30 | 0.2436 | Benchmark Baseline |

---

## ⚖️ Decision Support Logic

The decision module converts future price predictions into practical recommendations through a **Net Holding Return (NHR)** rule:

$$\text{NHR} = (\hat{P}_{t+h} - P_t) - (C_{\text{storage}} + C_{\text{spoilage}})$$

Where:

* $\hat{P}_{t+h}$ = Predicted forward modal price


* $P_t$ = Current APMC modal price


* $C_{\text{storage}}$ = Inventory holding cost per quintal
* $C_{\text{spoilage}}$ = Estimated loss rate from commodity deterioration

### Decision Policy

* **WAIT:** Triggered when $\text{NHR} > \theta$ (where threshold $\theta = ₹50/\text{qtl}$ buffer), indicating that anticipated price increases exceed storage and perishability risks.
* **SELL NOW:** Triggered when $\text{NHR} \le \theta$, signaling impending price drops, flat markets, or excessive holding costs.

---

## 📁 Project Structure

```text
AI-Based-Decision-Support-System/
│
├── app/
│   ├── app.py                     # Streamlit web interface and dashboard
│   ├── predict.py                 # Feature extraction and multi-model inference
│   └── market.py                  # APMC mandi ranking and recommendation logic
│
├── Models/
│   ├── models/
│   │   ├── onion_model.h5         # Trained Keras LSTM model for Onion
│   │   ├── tomato_rf.pkl          # Trained model for Tomato
│   │   └── potato_lr.pkl          # Trained model for Potato
│   │
│   └── scalers/
│       ├── onion_scaler.pkl       # MinMaxScaler for Onion sequence scaling
│       ├── tomato_scaler.pkl      # Scaler artifact for Tomato
│       └── potato_scaler.pkl      # Scaler artifact for Potato
│
├── data/
│   ├── Raw Data/
│   │   └── Agriculture_price_dataset.csv     # Raw AGMARKNET dataset
│   └── Processed Data/
│       └── Karnataka_Processed.csv           # Cleaned Karnataka records
│
├── Notebooks/
│   ├── 01_Data_Understanding.ipynb           # EDA and commodity price distributions
│   ├── 02_Preprocessing.ipynb                # Outlier filtering and date formatting
│   ├── 03_Model_Training.ipynb               # Deep learning LSTM sequence modeling
│   ├── 04_Model_Comparison.ipynb             # ML model benchmarking (LR, RF, GBR)
│   └── 05_Decision_Support_Engine.ipynb      # Decision rule and profit engine testing
│
├── Paper/
│   └── conference-template-a4.docx           # Academic research paper manuscript
│
├── requirements.txt                          # Production Python dependencies
├── runtime.txt                               # Environment specification
├── .gitignore
└── README.md

```

---

## ⚙️ Installation & Local Execution

### Prerequisites

* Python 3.11+
* Git

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

* **Language:** Python 3.11
* **Frontend / Deployment:** Streamlit, Streamlit Cloud
* **Machine Learning:** Scikit-learn, Joblib
* **Deep Learning:** TensorFlow / Keras (LSTM)
* **Data Processing & Analytics:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn

---

## 📄 License & Attribution

This project is licensed under the MIT License. The dataset is sourced from the Ministry of Agriculture & Farmers Welfare, Government of India (AGMARKNET).