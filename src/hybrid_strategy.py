import logging
from api_connection import place_order, get_balance
from src.state_machine import TradingStateMachine
from src.sma_calculations import fetch_and_calculate_sma
from src.pid_controller import PIDController
from tensorflow.keras.models import load_model

# Set up logging to file
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load the trained neural network model
model = load_model("models/price_prediction_model.h5")

# Initialize the state machine and PID controller
fsm = TradingStateMachine()
pid = PIDController(kp=0.1, ki=0.01, kd=0.05)

# Function to execute hybrid strategy
def hybrid_trading_strategy(pair, interval, pid, fsm, model):
    """
    Executes the hybrid trading strategy by combining state machine, PID controller, and SMA logic.

    Args:
        pair (str): Trading pair (e.g., 'XXRPZUSD').
        interval (int): Time interval for fetching historical prices (e.g., 1440 for 1 day).
        pid (PIDController): Initialized PID controller instance.
        fsm (TradingStateMachine): Initialized state machine instance.
        model: Neural network model for trend prediction.
    """
    # Step 1: Fetch and calculate SMA
    result = fetch_and_calculate_sma(pair, interval=interval, count=200)
    if result is None:
        logging.error("Error: Unable to calculate SMA. Skipping this cycle.")
        return

    sma_200 = result['sma']
    current_price = result['latest_price']

    # Step 2: Predict future trend using the neural network
    prediction = model.predict([[current_price, sma_200]])[0][0]

    # Step 3: Update the state machine based on current conditions
    state = fsm.update_state(current_price, sma_200, prediction)
    logging.debug(f"Updated State: {state}")

    # Step 4: Compute control signal using PID
    control_signal = pid.compute(sma_200, current_price)
    logging.debug(f"Control Signal: {control_signal}")

    # Step 5: Take action based on state and control signal
    if state == "Buying" and control_signal > 0:
        logging.info(f"Executing Buy Order for {abs(control_signal)} units.")
        # Simulating the buy order (you can use place_order() here for actual trading)
        print(f"Simulating Buy Order for {abs(control_signal)}")
        # place_order(pair, "buy", "market", str(abs(control_signal)))

    elif state == "Selling" and control_signal < 0:
        logging.info(f"Executing Sell Order for {abs(control_signal)} units.")
        # Simulating the sell order (you can use place_order() here for actual trading)
        print(f"Simulating Sell Order for {abs(control_signal)}")
        # place_order(pair, "sell", "market", str(abs(control_signal)))

def main():
    """
    Main execution loop for the hybrid trading strategy.
    """
    # Trading parameters
    pair = "XXRPZUSD"  # Example trading pair
    interval = 1440  # Daily interval (1 day)

    # Run the strategy in a loop
    import time
    while True:
        try:
            hybrid_trading_strategy(pair, interval, pid, fsm, model)
        except Exception as e:
            logging.error(f"Error: {e}")
        time.sleep(86400)  # Run once per day

if __name__ == "__main__":
    main()

# TESTING (COMMENTED OUT)
# if __name__ == "__main__":
#     fsm = TradingStateMachine()

#     test_cases = [
#         {"current_price": 2.2, "sma_200": 2.5, "prediction": 2.6},  # Expected: Buying
#         {"current_price": 2.8, "sma_200": 2.5, "prediction": 2.4},  # Expected: Selling
#         {"current_price": 2.6, "sma_200": 2.5, "prediction": 2.4},  # Expected: Waiting
#         {"current_price": 2.3, "sma_200": 2.5, "prediction": 2.8},  # Expected: Waiting
#     ]

#     for i, case in enumerate(test_cases, 1):
#         print(f"\nTest Case {i}:")
#         print(f"Current Price: {case['current_price']}, SMA: {case['sma_200']}, Prediction: {case['prediction']}")
#         updated_state = fsm.update_state(case["current_price"], case["sma_200"], case["prediction"])
#         print(f"Updated State: {updated_state}")
