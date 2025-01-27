import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import requests
from datetime import datetime

def fetch_historical_prices(pair, interval='1440', count=1000):
    """
    Fetch historical OHLC data from Kraken for the given trading pair.

    Args:
        pair (str): Trading pair (e.g., 'XRPUSD').
        interval (str): Interval for the OHLC data (default is 1440 for daily).
        count (int): Number of data points to fetch (default is 1000).

    Returns:
        list: List of closing prices.
    """
    url = f'https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}&count={count}'
    response = requests.get(url)
    data = response.json()

    if data.get('error'):
        raise ValueError(f"Error fetching data: {data['error']}")

    ohlc_data = data['result'][pair]
    prices = [float(item[4]) for item in ohlc_data]  # Close prices
    return prices

def calculate_sma(prices, window=200):
    """
    Calculate Simple Moving Average (SMA) for the given prices.

    Args:
        prices (list): List of historical prices.
        window (int): SMA window size.

    Returns:
        list: List of calculated SMAs.
    """
    sma = []
    for i in range(window, len(prices)):
        sma.append(np.mean(prices[i - window:i]))
    return sma

def generate_data(pair='XXRPZUSD', interval='1440', count=1000):
    """
    Fetches real historical data and calculates corresponding SMA and future prices.

    Args:
        pair (str): Trading pair (e.g., 'XRPUSD').
        interval (str): Interval for OHLC data (default is 1440 for 1-day).
        count (int): Number of data points to fetch.

    Returns:
        tuple: Features (X) and labels (y).
    """
    # Fetch historical prices from Kraken
    prices = fetch_historical_prices(pair, interval, count)
    smas = calculate_sma(prices)
    future_prices = prices[200:]  # For simplicity, use the last price as the future price
    
    # Combine price and SMA as features
    X = np.column_stack((prices[200:], smas))  # Prices and corresponding SMA
    y = future_prices  # Future prices as labels

    # Ensure that X and y are numpy arrays
    X = np.array(X)
    y = np.array(y)

    return X, y

def build_model():
    """
    Builds and compiles a simple feedforward neural network.
    """
    model = Sequential([
        Dense(64, input_dim=2, activation='relu'),  # Input: 2 features (price, SMA)
        Dense(32, activation='relu'),
        Dense(1, activation='linear')  # Output: Predicted future price
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
    return model

def train_and_save_model():
    """
    Trains the model on real market data and saves it to a file.
    """
    # Generate real market data
    X, y = generate_data(pair='XXRPZUSD', interval='1440', count=1000)

    # Build and train the model
    model = build_model()
    model.fit(X, y, epochs=50, batch_size=32, verbose=1)

    # Save the model
    model.save("models/price_prediction_model.h5")
    print("Model saved to models/price_prediction_model.h5")

if __name__ == "__main__":
    train_and_save_model()
