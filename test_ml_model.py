import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression

def create_test_dataset():
    """Create a test dataset with emissions data"""
    # Creating sample data
    data = {
        'fuel_type': ['Diesel', 'Petrol', 'Hybrid'] * 100,  # 300 samples
        'miles_driven': np.random.uniform(100, 1000, 300),
    }
    
    # Emission rates per mile
    emission_rates = {
        'Diesel': 0.27334,
        'Petrol': 0.26473,
        'Hybrid': 0.20288
    }
    
    # Calculate emissions
    data['emissions'] = [miles * emission_rates[fuel] 
                        for miles, fuel in zip(data['miles_driven'], data['fuel_type'])]
    
    return pd.DataFrame(data)

def train_model(df):
    """Train the ML model"""
    # Encode fuel types
    le = LabelEncoder()
    fuel_encoded = le.fit_transform(df['fuel_type'])
    
    # Prepare features and target
    X = np.column_stack((fuel_encoded, df['miles_driven']))
    y = df['emissions']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model, le

def predict_emissions(model, le, fuel_type, miles):
    """Predict emissions for given fuel type and miles"""
    fuel_encoded = le.transform([fuel_type])[0]
    prediction = model.predict([[fuel_encoded, miles]])
    return round(prediction[0], 3)

# Test the model
if __name__ == "__main__":
    # Create and display dataset
    df = create_test_dataset()
    print("\nDataset Sample:")
    print(df.head())
    
    # Train model
    model, label_encoder = train_model(df)
    
    # Test predictions
    while True:
        print("\nEmissions Calculator")
        print("-------------------")
        print("Available fuel types: Diesel, Petrol, Hybrid")
        
        try:
            fuel = input("Enter fuel type (or 'exit' to quit): ").capitalize()
            if fuel.lower() == 'exit':
                break
                
            if fuel not in ['Diesel', 'Petrol', 'Hybrid']:
                print("Invalid fuel type!")
                continue
                
            miles = float(input("Enter miles driven: "))
            if miles < 0:
                print("Miles cannot be negative!")
                continue
                
            emissions = predict_emissions(model, label_encoder, fuel, miles)
            print(f"\nPredicted CO2 emissions: {emissions} kg")
            
        except ValueError:
            print("Invalid input! Please enter a number for miles.")
        except Exception as e:
            print(f"An error occurred: {e}")