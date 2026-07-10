# 🌾 AI-Based Decision Support System for Agricultural Price Prediction and Market Recommendation

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

## 📂 Project Structure

```text
AI-Based-Decision-Support-System
│
├── app/
│   ├── app.py
│   ├── predict.py
│   └── market.py
│
├── data/
│   ├── Processed Data/
│   └── Raw Data/
│
├── Models/
│   ├── models/
│   └── scalers/
│
├── Notebooks/
│
├── Paper/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

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

## 📷 Screenshots

The following screenshots will be added after deployment.

- Home Page
- Prediction Result
- Profit Analysis
- Recommended Market
- Top 10 Market Comparison

---

## 🔮 Future Enhancements

- Multi-state agricultural market support
- Weather-based prediction
- Mobile application
- Multi-language interface
- Real-time API integration
- Additional crop support

---

## 📄 License

This project is intended for educational and research purposes.
