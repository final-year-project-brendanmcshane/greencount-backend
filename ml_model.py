import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Temporary function to load a dataset
def load_dataset(file_path):
    """Loads the emissions dataset into a pandas DataFrame."""
    try:
        df = pd.read_csv(file_path)
        print("Dataset loaded successfully!")
        print(df.head())  # Print first few rows to check structure
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

# Temporary test dataset (you can remove this when you have the real CSV)
def create_test_dataset():
    """Creates a small test dataset for emissions."""
    data = {
        "Energy_Consumption_kWh": [100, 200, 150, 300, 250],
        "Emissions_kgCO2": [23, 46, 34, 69, 57]  # Sample emission values
    }
    df = pd.DataFrame(data)
    df.to_csv("test_emissions.csv", index=False)  # Save locally for testing
    return df

# Train the model
def train_model(df):
    """Trains a Linear Regression model on energy consumption vs. emissions."""
    print("\nTraining the model...")

    # Extract features (X) and target variable (y)
    X = df[['Energy_Consumption_kWh']]  # Independent variable
    y = df['Emissions_kgCO2']  # Dependent variable

    # Initialize and train the model
    model = LinearRegression()
    model.fit(X, y)

    print("Model training complete!")
    print(f"Model Coefficient (slope): {model.coef_[0]}")
    print(f"Model Intercept: {model.intercept_}")

    return model

# Predict emissions
def predict_emissions(model, energy_consumption):
    """Predicts CO2 emissions for a given energy consumption value."""
    input_df = pd.DataFrame({"Energy_Consumption_kWh": [energy_consumption]})
    prediction = model.predict(input_df)
    return round(prediction[0], 2)  # ✅ Now it rounds to 2 decimal places



# ✅ Create and load test dataset
test_df = create_test_dataset()
print("Test dataset created.")

loaded_df = load_dataset("test_emissions.csv")
if loaded_df is not None:
    trained_model = train_model(loaded_df)  # Train model

    # Example Prediction
    while True:
        user_input = input("\nEnter energy consumption in kWh (or type 'exit' to quit): ")
    
        if user_input.lower() == 'exit':
            print("Exiting program.")
            break

        try:
            test_value = float(user_input)  # Convert user input to float
            predicted_emission = predict_emissions(trained_model, test_value)
            print(f"Predicted emissions for {test_value} kWh: {predicted_emission} kgCO2")
        except ValueError:
            print("⚠️ Invalid input. Please enter a number.")
