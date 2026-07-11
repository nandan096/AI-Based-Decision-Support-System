# 🌾 AI-Based Decision Support System for Agricultural Price Prediction and Market Recommendation

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-LSTM-orange?logo=tensorflow)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?logo=scikitlearn)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌐 Live Demo

👉 **[Launch Application](https://ai-based-decision-support-system.streamlit.app/)**

## 💻 GitHub Repository

👉 **[View Source Code](https://github.com/nandan096/AI-Based-Decision-Support-System)**

## 📌 Project Overview

This project presents an AI-Based Decision Support System that assists farmers in making informed agricultural marketing decisions by predicting crop prices and recommending the best market for selling their produce.

Unlike traditional systems that use a single machine learning model, this project adopts a hybrid approach by selecting the best-performing model for each crop to improve prediction accuracy.

The application is developed using Streamlit and provides an interactive interface for farmers to estimate future prices, analyze expected profit, and identify the most suitable market based on historical agricultural price data.

---

## 🚀 Features

- 🌾 Crop Price Prediction
- 🤖 Hybrid AI Model Selection
- 📊 Dynamic Historical Data Processing
- 💰 Farmer Profit Analysis
- 🏪 Best Market Recommendation
- 📈 Sell / Wait Decision Support
- 📱 Interactive Streamlit Dashboard

---

## 🧠 Machine Learning Models

| Crop   | Model Used        |
| ------ | ----------------- |
| Onion  | LSTM              |
| Tomato | Random Forest     |
| Potato | Linear Regression |

The system automatically selects the appropriate model depending on the selected crop.

---

## 🛠 Technologies Used

- Python
- Streamlit
- TensorFlow / Keras
- Scikit-learn
- Pandas
- NumPy
- Joblib

---

## 📁 Project Structure

```text
AI-Based-Decision-Support-System/
│
├── app/
│   ├── app.py                 # Streamlit application
│   ├── predict.py             # Price prediction module
│   └── market.py              # Market recommendation logic
│
├── Models/
│   ├── models/
│   │   ├── onion_model.h5
│   │   ├── tomato_rf.pkl
│   │   └── potato_lr.pkl
│   │
│   └── scalers/
│       ├── onion_scaler.pkl
│       ├── tomato_scaler.pkl
│       └── potato_scaler.pkl
│
├── data/
│   ├── Raw Data/
│   └── Processed Data/
│
├── Notebooks/
│   ├── 01_Data_Understanding.ipynb
│   ├── 02_Preprocessing.ipynb
│   ├── 03_Model_Training.ipynb
│   ├── 04_Model_Comparison.ipynb
│   └── 05_Decision_Support_Engine.ipynb
│
├── requirements.txt
├── runtime.txt
└── README.md
```

## 🔄 Project Workflow

```text
Historical Market Data
          │
          ▼
Data Preprocessing
          │
          ▼
Crop Selection
          │
          ▼
Hybrid Model Selection
   ├── Onion  → LSTM
   ├── Tomato → Random Forest
   └── Potato → Linear Regression
          │
          ▼
Price Prediction
          │
          ▼
Profit Analysis
          │
          ▼
Market Recommendation
          │
          ▼
Streamlit Dashboard
```


## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/AI-Based-Decision-Support-System.git
```

Move into the project folder:

```bash
cd AI-Based-Decision-Support-System
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app/app.py
```

---

## 📊 Application Workflow

1. Select the crop.
2. Enter quantity and production cost.
3. Click **Predict**.
4. The system:
   - Loads the latest historical data.
   - Selects the best machine learning model.
   - Predicts the future price.
   - Calculates expected profit.
   - Provides Sell / Wait recommendation.
   - Recommends the best market.

---


## 🔮 Future Enhancements

- Multi-state agricultural market support
- Weather-based prediction
- Mobile application
- Multi-language interface
- Real-time API integration
- Additional crop support

---
## 📌 Summary

This project demonstrates the application of Machine Learning, Deep Learning, and Decision Support Systems to solve a real-world agricultural problem. By integrating multiple predictive models with an interactive Streamlit dashboard, the system assists users in making informed crop marketing decisions through price forecasting, profit estimation, and market recommendations.

## 📄 License

This project is intended for educational and research purposes.
