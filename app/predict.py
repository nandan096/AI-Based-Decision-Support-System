import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

# -------------------------------
# 1. Load Trained Models
# -------------------------------
onion_model = load_model('Models/models/onion_model.h5', compile=False)

onion_scaler = joblib.load('Models/scalers/onion_scaler.pkl')

tomato_model = joblib.load('Models/models/tomato_rf.pkl')

potato_model = joblib.load('Models/models/potato_lr.pkl')


# -------------------------------
# 2. Prediction Function
# -------------------------------
def predict_price(last_30_prices, crop):
  crop = crop.lower()

  # ---------------- Onion (LSTM) ----------------
  if crop == 'onion':
    prices = np.array(last_30_prices).reshape(-1, 1)
    scaled = onion_scaler.transform(prices)
    X = scaled.reshape(1, 30, 1)

    prediction = onion_model.predict(X, verbose=0)
    predicted_price = onion_scaler.inverse_transform(prediction)
    return float(predicted_price[0][0])

  # ---------------- Tomato (High-Accuracy Lag Model) ----------------
  elif crop == 'tomato':
    # Extract 4 features: Lag_1, Lag_2, Lag_3, Rolling_3
    lag_1 = last_30_prices[-1]
    lag_2 = last_30_prices[-2]
    lag_3 = last_30_prices[-3]
    rolling_3 = float(np.mean(last_30_prices[-3:]))

    X = np.array([[lag_1, lag_2, lag_3, rolling_3]])
    prediction = tomato_model.predict(X)
    return float(prediction[0])

  # ---------------- Potato (High-Accuracy Memory Model) ----------------
  elif crop == 'potato':
    # Extract 5 features: Lag_1, Lag_2, Lag_7, Rolling_7, Month
    lag_1 = last_30_prices[-1]
    lag_2 = last_30_prices[-2]
    lag_7 = last_30_prices[-7]
    rolling_7 = float(np.mean(last_30_prices[-7:]))
    month = int(pd.Timestamp.now().month)

    X = np.array([[lag_1, lag_2, lag_7, rolling_7, month]])
    prediction = potato_model.predict(X)
    return float(prediction[0])

  else:
    raise ValueError('Invalid Crop Selected')