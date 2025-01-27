class PIDController:
    def __init__(self, kp, ki, kd):
        """
        Initialize PID controller with given coefficients.

        Args:
            kp (float): Proportional gain.
            ki (float): Integral gain.
            kd (float): Derivative gain.
        """
        self.kp = kp  # Proportional term coefficient
        self.ki = ki  # Integral term coefficient
        self.kd = kd  # Derivative term coefficient
        self.prev_error = 0  # Previous error for derivative calculation
        self.integral = 0  # Cumulative error for integral calculation

    def compute(self, setpoint, current_value):
        """
        Compute the control signal based on the PID formula.

        Args:
            setpoint (float): Target value (e.g., SMA or desired price level).
            current_value (float): Current value (e.g., current price).

        Returns:
            float: Control signal (e.g., trade volume adjustment).
        """
        # Calculate error
        error = setpoint - current_value

        # Update integral (sum of errors over time)
        self.integral += error

        # Calculate derivative (rate of change of error)
        derivative = error - self.prev_error

        # Compute the control signal
        control_signal = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)

        # Update the previous error
        self.prev_error = error

        return control_signal

    def __str__(self):
        """String representation of the PID controller state."""
        return f"PIDController(kp={self.kp}, ki={self.ki}, kd={self.kd})"

# TESTING (Optional)
#if __name__ == "__main__":
 #   pid = PIDController(kp=0.1, ki=0.01, kd=0.05)

    # Simulated test cases
  #  test_cases = [
   #     {"setpoint": 2.5, "current_value": 2.3},  # Positive error
    #    {"setpoint": 2.5, "current_value": 2.7},  # Negative error
     #   {"setpoint": 2.5, "current_value": 2.5},  # Zero error
    #]

    #for i, case in enumerate(test_cases, 1):
     #   print(f"\nTest Case {i}:")
      #  print(f"Setpoint: {case['setpoint']}, Current Value: {case['current_value']}")
       # control_signal = pid.compute(case["setpoint"], case["current_value"])
       # print(f"Control Signal: {control_signal}")
