import os
from dotenv import load_dotenv
import krakenex

# Load environment variables
load_dotenv()

API_KEY = os.getenv('KRAKEN_API_KEY')
API_SECRET = os.getenv('KRAKEN_API_SECRET')

kraken = krakenex.API()
kraken.key = API_KEY
kraken.secret = API_SECRET

# Get account balance
def get_balance():
    response = kraken.query_private('Balance')
    if response['error']:
        print("Error:", response['error'])
    else:
        print("Balance:", response['result'])

# Place an order
def place_order(pair, type, ordertype, volume, price=None):
    order_data = {
        'pair': pair,
        'type': type,  # 'buy' or 'sell'
        'ordertype': ordertype,  # 'market' or 'limit'
        'volume': volume,
    }
    if price:  # Add price only for limit orders
        order_data['price'] = price

    response = kraken.query_private('AddOrder', order_data)
    if response['error']:
        print("Error:", response['error'])
    else:
        print("Order Result:", response['result'])

# Get open orders
def get_open_orders():
    response = kraken.query_private('OpenOrders')
    print("Open Orders:", response)

# Get closed orders
def get_closed_orders():
    response = kraken.query_private('ClosedOrders')
    print("Closed Orders:", response)

if __name__ == "__main__":
    # Test the functions here
    print("Checking account balance:")
    get_balance()
    
    print("\nPlacing a test order:")
    place_order('XXRPZUSD', 'buy', 'market', '2')  # Buy 2 XRP at market price
    
    print("\nRetrieving closed orders:")
    get_closed_orders()
