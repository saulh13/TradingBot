import os
import logging
import time
from dotenv import load_dotenv
import krakenex

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('KRAKEN_API_KEY')
API_SECRET = os.getenv('KRAKEN_API_SECRET')

# Set up Kraken API client
kraken = krakenex.API()
kraken.key = API_KEY
kraken.secret = API_SECRET

# Set up logging to file
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Retry mechanism for API calls
def safe_query_private(endpoint, data=None, retries=3, delay=5):
    """Wrapper for Kraken's query_private with retry mechanism."""
    for attempt in range(retries):
        try:
            response = kraken.query_private(endpoint, data)
            if not response['error']:
                return response
            logging.error(f"Attempt {attempt + 1} failed for {endpoint}: {response['error']}")
            time.sleep(delay)
        except Exception as e:
            logging.error(f"Exception during API call to {endpoint}: {e}")
    logging.critical(f"All {retries} attempts failed for {endpoint}.")
    return None

# Get account balance
def get_balance():
    """
    Fetches the account balance from Kraken.

    Returns:
        dict: Account balances (e.g., {'ZUSD': '100', 'XXRP': '50'}).
    """
    response = safe_query_private('Balance')
    if response:
        logging.info("Fetched account balance successfully.")
        return response['result']
    return None

# Place an order
def place_order(pair, type, ordertype, volume, price=None):
    """
    Places an order on Kraken.

    Args:
        pair (str): Trading pair (e.g., 'XRPUSD').
        type (str): Order type ('buy' or 'sell').
        ordertype (str): Market or limit order.
        volume (str): Amount to trade.
        price (str, optional): Price for limit orders. Defaults to None.

    Returns:
        dict: API response with order details, or None if the order fails.
    """
    order_data = {
        'pair': pair,
        'type': type,  # 'buy' or 'sell'
        'ordertype': ordertype,  # 'market' or 'limit'
        'volume': volume,
    }
    if price:
        order_data['price'] = price

    response = safe_query_private('AddOrder', order_data)
    if response:
        if response['error']:
            logging.error(f"Order placement error: {response['error']}")
        else:
            logging.info(f"Order placed successfully: {response['result']}")
        return response['result']
    return None

# Get open orders
def get_open_orders():
    """
    Fetches all open orders on Kraken.

    Returns:
        dict: Open orders or None if fetching data fails.
    """
    response = safe_query_private('OpenOrders')
    if response:
        logging.info("Fetched open orders successfully.")
        return response['result']
    return None

# Get closed orders
def get_closed_orders():
    """
    Fetches all closed orders on Kraken.

    Returns:
        dict: Closed orders or None if fetching data fails.
    """
    response = safe_query_private('ClosedOrders')
    if response:
        logging.info("Fetched closed orders successfully.")
        return response['result']
    return None



####
# Main function for testing 
if __name__ == "__main__":
    print("Checking account balance...")
    balance = get_balance()
    if balance:
        print("Balance:", balance)
    else:
        print("Failed to retrieve balance.")
# Main function for testing 
if __name__ == "__main__":
    print("Checking account balance...")
    balance = get_balance()
    print("Balance:", balance)

#Placing a test order (e.g., buying 1 XRP)
    print("\nPlacing a test order...")
    test_order = place_order('XRPUSD', 'buy', 'market', '1')  # Buy 1 XRP at market price
    print("Order Result:", test_order)