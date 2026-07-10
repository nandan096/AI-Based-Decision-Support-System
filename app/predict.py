import joblib
import numpy as np
from tensorflow.keras.models import load_model

# -------------------------------
# Onion (LSTM)
# -------------------------------
onion_model = load_model(
    "Models/models/onion_model.h5",
    compile=False
)

onion_scaler = joblib.load(
    "Models/scalers/onion_scaler.pkl"
)

# -------------------------------
# Tomato (Random Forest)
# -------------------------------
tomato_model = joblib.load(
    "Models/models/tomato_rf.pkl"
)

# -------------------------------
# Potato (Linear Regression)
# -------------------------------
potato_model = joblib.load(
    "Models/models/potato_lr.pkl"
)


def predict_price(last_30_prices, crop):

    crop = crop.lower()

    # ---------------- Onion ----------------
    if crop == "onion":

        prices = np.array(last_30_prices).reshape(-1, 1)

        scaled = onion_scaler.transform(prices)

        X = scaled.reshape(1, 30, 1)

        prediction = onion_model.predict(X, verbose=0)

        predicted_price = onion_scaler.inverse_transform(prediction)

        return float(predicted_price[0][0])

    # ---------------- Tomato ----------------
    elif crop == "tomato":

        X = np.array(last_30_prices).reshape(1, -1)

        prediction = tomato_model.predict(X)

        return float(prediction[0])

    # ---------------- Potato ----------------
    elif crop == "potato":

        X = np.array(last_30_prices).reshape(1, -1)

        prediction = potato_model.predict(X)

        return float(prediction[0])

    else:
        raise ValueError("Invalid Crop Selected")