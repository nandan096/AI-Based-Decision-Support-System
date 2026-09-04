import joblib
import numpy as np
import pandas as pd

# -------------------------------------------------------------
# 1. Load Selected Winning Models
# -------------------------------------------------------------
onion_model = joblib.load('Models/models/onion_lr.pkl')
tomato_model = joblib.load('Models/models/tomato_lr.pkl')
potato_model = joblib.load('Models/models/potato_gb.pkl')


# -------------------------------------------------------------
# 2. Prediction Inference Function
# -------------------------------------------------------------
def predict_price(last_30_prices, crop, month=6):
  crop = crop.lower()

  # Onion: Linear Regression (Lag 1, Lag 2, Lag 7, Rolling 7, Month)
  if crop == 'onion':
    lag_1 = last_30_prices[-1]
    lag_2 = last_30_prices[-2]
    lag_7 = last_30_prices[-7]
    rolling_7 = float(np.mean(last_30_prices[-7:]))

    X = np.array([[lag_1, lag_2, lag_7, rolling_7, month]])
    prediction = onion_model.predict(X)
    return float(prediction[0])

  # Tomato: Linear Regression (Lag 1, Lag 2, Lag 3, Rolling 3)
  elif crop == 'tomato':
    lag_1 = last_30_prices[-1]
    lag_2 = last_30_prices[-2]
    lag_3 = last_30_prices[-3]
    rolling_3 = float(np.mean(last_30_prices[-3:]))

    X = np.array([[lag_1, lag_2, lag_3, rolling_3]])
    prediction = tomato_model.predict(X)
    return float(prediction[0])

  # Potato: Gradient Boosting (Lag 1, Lag 2, Lag 7, Rolling 7, Month)
  elif crop == 'potato':
    lag_1 = last_30_prices[-1]
    lag_2 = last_30_prices[-2]
    lag_7 = last_30_prices[-7]
    rolling_7 = float(np.mean(last_30_prices[-7:]))

    X = np.array([[lag_1, lag_2, lag_7, rolling_7, month]])
    prediction = potato_model.predict(X)
    return float(prediction[0])

  else:
    raise ValueError('Invalid Crop Selected')