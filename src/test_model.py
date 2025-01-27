import logging
import numpy as np
from tensorflow.keras.models import load_model
from sma_calculations import fetch_and_calculate_sma
import requests

# Set up logging
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load the trained neural network model
model = load_model("models/price_prediction_model.h5")

# Function to fetch historical prices and calculate SMA
def test_model(pair='XXRPZUSD', interval='1440', count=200):
    """
    Test the model using real data from Kraken.

    Args:
        pair (str): Trading pair (e.g., 'XRPUSD').
        interval (str): Time interval for OHLC data (default is 1440 for 1 day).
        count (int): Number of data points to fetch.

    Returns:
        list: Predictions and actual prices for comparison.
    """
    # Step 1: Fetch historical data and calculate SMA
    result = fetch_and_calculate_sma(pair, interval, count)
    if result is None:
        logging.error("Error: Unable to calculate SMA. Exiting testing.")
        return

    sma_200 = result['sma']
    current_price = result['latest_price']

    # Step 2: Prepare the input data (latest price and SMA) for prediction
    input_data = np.array([[current_price, sma_200]])

    # Step 3: Predict the future price
    try:
        prediction = model.predict(input_data)
        predicted_price = prediction[0][0]

        # Log and print the results
        logging.info(f"Predicted Price: {predicted_price}, Actual Price: {current_price}")
        print(f"Predicted Price: {predicted_price}, Actual Price: {current_price}")

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        print(f"Error during prediction: {e}")

# Run the test
test_model(pair='XXRPZUSD', interval='1440', count=200)
