#BELOW IS JUST SAMPLE CODE I DID NOT IMPLEMENT INTO THIS PROJECT


import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

#Link to UK Government dataset https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2024

# Load and Analyze UK Government Emissions Dataset First
print("\n🚀 Starting UK Emissions Dataset Analysis...")  # Debug Print

def analyze_uk_emissions(file_path):
    """Loads and analyzes the UK emissions dataset."""
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()  # Clean column names

        print("✅ Dataset loaded successfully!")
        print("\n📝 Column Names:", df.columns.tolist())
        print("\n🔍 Unique Activities (first 20):")
        print(df['Activity'].unique()[:20])  # Show first 20 unique activities

        return df
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None

# Run UK Emissions Analysis
uk_emissions_df = analyze_uk_emissions(r"C:\Users\brend\Desktop\emissions.csv")

if uk_emissions_df is not None:
    print("\n✅ Successfully loaded and analyzed UK emissions dataset!")
else:
    print("\n❌ Failed to load UK emissions dataset. Check file path or format.")

def explore_dataset(df):
    """Prints dataset structure and unique values for key columns."""
    print("\n📌 Column Names:\n", df.columns.tolist())

    # Print unique values in key columns to understand what's inside
    for col in df.columns:
        unique_values = df[col].dropna().unique()[:10]  # Show first 10 unique values
        print(f"\n🔍 Unique values in '{col}' (first 10):\n", unique_values)

# Run this function
if uk_emissions_df is not None:
    explore_dataset(uk_emissions_df)


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

# Load the UK Government emissions dataset
def load_uk_emissions(file_path):
    """Loads and displays the first few rows of the UK emissions dataset."""
    try:
        df = pd.read_csv(file_path)

        # Strip any leading or trailing spaces from column names
        df.columns = df.columns.str.strip()

        print("Dataset loaded successfully!")
        print("\nColumn Names:", df.columns.tolist())  # Print column names for reference
        print(df.head(10))  # Show first few rows

        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

# Example usage
uk_emissions_df = load_uk_emissions(r"C:\Users\brend\Desktop\emissions.csv")

def analyze_uk_emissions(file_path):
    """Loads and analyzes the UK emissions dataset."""
    try:
        df = pd.read_csv(file_path)

        # Strips any leading/trailing spaces from column names
        df.columns = df.columns.str.strip()

        print("✅ Dataset loaded successfully!")
        print("\n📝 Column Names:", df.columns.tolist())  # Prints column names for reference

        print("\n🔍 Unique Activities (first 20):")
        print(df['Activity'].unique()[:20])  # Print first 20 unique activities to explore data

        return df
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None

# Run this function
uk_emissions_df = analyze_uk_emissions(r"C:\Users\brend\Desktop\emissions.csv")

def load_and_check_dataset(file_path):
    """Loads the dataset and prints basic info."""
    try:
        df = pd.read_csv(file_path)

        # Remove extra spaces from column names
        df.columns = df.columns.str.strip()

        print("✅ Dataset loaded successfully!")
        print("\n📌 First 10 rows:")
        print(df.head(10))  # Show first 10 rows

        print("\n📌 Column Names:")
        print(df.columns.tolist())  # Show all column names

        print("\n📌 Unique 'Activity' values (first 20):")
        print(df['Activity'].unique()[:20])  # Show first 20 unique activities

        return df
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None

