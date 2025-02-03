import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression

def create_test_dataset():
    """Create test dataset with vehicle and energy emissions"""
    num_samples = 300
    data = {
        'type': ['Car', 'Car', 'Car', 'Energy'] * 75,  # 300 samples total
        'subtype': ['Diesel', 'Petrol', 'Hybrid', 'Electricity'] * 75,
        'amount': np.random.uniform(100, 1000, num_samples),  # miles or kWh
    }
    
    # Emission rates
    emission_rates = {
        ('Car', 'Diesel'): 0.27334,      # per mile
        ('Car', 'Petrol'): 0.26473,      # per mile
        ('Car', 'Hybrid'): 0.20288,      # per mile
        ('Energy', 'Electricity'): 0.20705  # per kWh (2024 UK rate)
    }
    
    # Calculate emissions
    data['emissions'] = [amount * emission_rates[(type_, subtype)] 
                        for type_, subtype, amount in zip(data['type'], data['subtype'], data['amount'])]
    
    return pd.DataFrame(data)

def train_model(df):
    """Train ML model"""
    # Encode categorical variables
    le_type = LabelEncoder()
    le_subtype = LabelEncoder()
    
    type_encoded = le_type.fit_transform(df['type'])
    subtype_encoded = le_subtype.fit_transform(df['subtype'])
    
    # Prepare features and target
    X = np.column_stack((type_encoded, subtype_encoded, df['amount']))
    y = df['emissions']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model, le_type, le_subtype

def predict_emissions(model, le_type, le_subtype, type_, subtype, amount):
    """Predict emissions"""
    type_encoded = le_type.transform([type_])[0]
    subtype_encoded = le_subtype.transform([subtype])[0]
    prediction = model.predict([[type_encoded, subtype_encoded, amount]])
    return round(prediction[0], 3)

if __name__ == "__main__":
    # Create and display dataset
    df = create_test_dataset()
    print("\nDataset Sample:")
    print(df.head())
    
    # Train model
    model, le_type, le_subtype = train_model(df)
    
    # Test predictions
    while True:
        print("\nEmissions Calculator")
        print("-------------------")
        print("Available types: Car, Energy")
        print("Car subtypes: Diesel, Petrol, Hybrid")
        print("Energy subtypes: Electricity")
        
        try:
            type_ = input("Enter type (or 'exit' to quit): ").capitalize()
            if type_.lower() == 'exit':
                break
                
            subtype = input("Enter subtype: ").capitalize()
            if type_ == 'Car':
                amount = float(input("Enter miles driven: "))
            else:
                amount = float(input("Enter electricity used (kWh): "))
            
            emissions = predict_emissions(model, le_type, le_subtype, type_, subtype, amount)
            print(f"\nPredicted CO2 emissions: {emissions} kg")
            
        except ValueError:
            print("Invalid input! Please check your values.")
        except Exception as e:
            print(f"An error occurred: {e}")

