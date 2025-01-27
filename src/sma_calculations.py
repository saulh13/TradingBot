import requests

def calculate_sma(prices, window=200):
    """
    Calculates the Simple Moving Average (SMA) for the given prices.

    Args:
        prices (list): List of historical prices.
        window (int): The SMA window size (default is 200).

    Returns:
        float: The SMA value, or None if there is not enough data.
    """
    if len(prices) < window:
        return None  # Not enough data to calculate SMA
    return sum(prices[-window:]) / window

def fetch_historical_prices(pair, interval=1440, count=200):
    """
    Fetches historical OHLC prices from the Kraken API.

    Args:
        pair (str): Trading pair (e.g., 'XXRPZUSD').
        interval (int): Time interval for OHLC data (default is 1440 minutes for 1 day).
        count (int): Number of data points to fetch.

    Returns:
        list: A list of closing prices, or None if fetching data fails.
    """
    url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}&count={count}"
    response = requests.get(url)
    data = response.json()
    if response.status_code != 200 or 'error' in data and data['error']:
        print(f"Error fetching data: {data.get('error', [])}")
        return None
    ohlc = data['result'][pair]
    return [float(row[4]) for row in ohlc]  # Extract closing prices

def fetch_and_calculate_sma(pair, interval=1440, count=200):
    """
    Fetches historical prices and calculates the SMA.

    Args:
        pair (str): Trading pair (e.g., 'XXRPZUSD').
        interval (int): Time interval for OHLC data (default is 1440 minutes for 1 day).
        count (int): Number of data points to fetch.

    Returns:
        dict: A dictionary containing the SMA and the latest price, or None if an error occurs.
    """
    historical_prices = fetch_historical_prices(pair, interval=interval, count=count)
    if not historical_prices:
        print("Error: Unable to fetch historical prices.")
        return None
    sma = calculate_sma(historical_prices, window=200)
    if sma is None:
        print("Error: Not enough data to calculate SMA.")
        return None
    return {"sma": sma, "latest_price": historical_prices[-1]}


# TESTING PART
if __name__ == "__main__":
    # Test configuration
    pair = "XXRPZUSD"  # Example trading pair
    interval = 1440  # Daily interval (1 day)

    # Fetch and calculate SMA
    result = fetch_and_calculate_sma(pair, interval=interval, count=200)
    if result:
        print(f"200-day SMA: {result['sma']}")
        print(f"Latest Price: {result['latest_price']}")
    else:
        print("Error: Failed to fetch or calculate SMA.")
