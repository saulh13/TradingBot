class TradingStateMachine:
    def __init__(self):
        self.state = "Waiting"

    def update_state(self, current_price, sma_200, prediction):
        """
        Update the state of the trading bot based on current price,
        SMA, and neural network prediction.

        Args:
            current_price (float): The current market price.
            sma_200 (float): The 200-day Simple Moving Average.
            prediction (float): Neural network prediction of future price trend.

        Returns:
            str: The updated state.
        """
        # Debugging information
        print(f"DEBUG: Current State: {self.state}")
        print(f"DEBUG: Current Price: {current_price}, SMA: {sma_200}, Prediction: {prediction}")

        if self.state == "Waiting":
            if current_price < sma_200 * 0.9 and prediction > current_price:
                print("DEBUG: Transitioning to Buying...")
                self.state = "Buying"
            elif current_price > sma_200 * 1.1 and prediction < current_price:
                print("DEBUG: Transitioning to Selling...")
                self.state = "Selling"

        elif self.state == "Buying":
            # Recheck if conditions for Selling arise while in Buying
            if current_price > sma_200 * 1.1 and prediction < current_price:
                print("DEBUG: Re-evaluating: Transitioning to Selling...")
                self.state = "Selling"
            else:
                print("DEBUG: Transitioning to Holding after Buying...")
                self.state = "Holding"

        elif self.state == "Selling":
            # Recheck if conditions for Buying arise while in Selling
            if current_price < sma_200 * 0.9 and prediction > current_price:
                print("DEBUG: Re-evaluating: Transitioning to Buying...")
                self.state = "Buying"
            else:
                print("DEBUG: Transitioning to Holding after Selling...")
                self.state = "Holding"

        elif self.state == "Holding":
            print("DEBUG: Transitioning to Waiting after Holding...")
            self.state = "Waiting"

        return self.state

    def __str__(self):
        """String representation of the current state."""
        return f"Current State: {self.state}"

# TESTING #
if __name__ == "__main__":
    fsm = TradingStateMachine()

    test_cases = [
        # Case 1: Price is 10% below the SMA, prediction is higher (should trigger Buy)
        {"current_price": 2.2, "sma_200": 2.5, "prediction": 2.6},  # Expected: Buying

        # Case 2: Price is 10% above the SMA, prediction is lower (should trigger Sell)
        {"current_price": 2.8, "sma_200": 2.5, "prediction": 2.4},  # Expected: Selling

        # Case 3: Price is close to the SMA, prediction is lower (should remain Waiting)
        {"current_price": 2.6, "sma_200": 2.5, "prediction": 2.4},  # Expected: Waiting

        # Case 4: Price is below the SMA and prediction is higher (still should not buy yet)
        {"current_price": 2.3, "sma_200": 2.5, "prediction": 2.8},  # Expected: Waiting
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Current Price: {case['current_price']}, SMA: {case['sma_200']}, Prediction: {case['prediction']}")
        updated_state = fsm.update_state(case["current_price"], case["sma_200"], case["prediction"])
        print(f"Updated State: {updated_state}")
