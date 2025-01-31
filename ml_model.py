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

# Create and load the test dataset
test_df = create_test_dataset()
print("Test dataset created.")
print(test_df)
