import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

def build_model():
    """
    Builds and compiles a simple feedforward neural network.

    Returns:
        keras.Model: Compiled Keras model.
    """
    model = Sequential([
        Dense(64, input_dim=2, activation='relu'),  # Input: 2 features (price, SMA)
        Dense(32, activation='relu'),
        Dense(1, activation='linear')  # Output: Predicted future price
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
    return model

def generate_sample_data(num_samples=1000):
    """
    Generates synthetic data for training the model.

    Args:
        num_samples (int): Number of training samples.

    Returns:
        tuple: Features (X) and labels (y).
    """
    np.random.seed(42)
    prices = np.random.uniform(1, 10, size=num_samples)  # Simulated prices
    smas = prices + np.random.normal(0, 0.5, size=num_samples)  # Simulated SMA
    future_prices = prices + np.random.normal(0, 0.2, size=num_samples)  # Simulated future prices
    X = np.column_stack((prices, smas))  # Combine price and SMA as features
    y = future_prices  # Future prices as labels
    return X, y

def train_and_save_model():
    """
    Trains the model on synthetic data and saves it to a file.
    """
    # Generate synthetic data
    X, y = generate_sample_data()

    # Build the model
    model = build_model()

    # Train the model
    print("Training the model...")
    model.fit(X, y, epochs=50, batch_size=32, verbose=1)

    # Save the model
    model.save("models/price_prediction_model.h5")
    print("Model saved to models/price_prediction_model.h5")

if __name__ == "__main__":
    # Train and save the model
    train_and_save_model()

    # Load the saved model for testing
    #model = load_model("models/price_prediction_model.h5")

    # Test the model with new data
    ##prices = np.array([5.5, 6.2, 7.0])  # Example prices
    #smas = np.array([5.6, 6.1, 7.1])    # Example SMAs
    #X_test = np.column_stack((prices, smas))

    # Predict future prices
    #predictions = model.predict(X_test)

    # Display the results
    #print("\n## Model Predictions ##")
    #for i, prediction in enumerate(predictions):
     #   print(f"Input: Price={prices[i]}, SMA={smas[i]} | Predicted Future Price: {prediction[0]:.2f}")
