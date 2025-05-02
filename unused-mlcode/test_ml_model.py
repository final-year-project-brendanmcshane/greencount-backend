#BELOW IS JUST SAMPLE CODE I DID NOT IMPLEMENT INTO THIS PROJECT

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

def create_training_dataset():
    """Create training dataset from emissions conversion factors"""
    # Define the emission rates from your dataset
    data = [
        # Cars
        {'category': 'Car', 'type': 'Diesel', 'unit': 'mile', 'rate': 0.27334},
        {'category': 'Car', 'type': 'Petrol', 'unit': 'mile', 'rate': 0.26473},
        {'category': 'Car', 'type': 'Hybrid', 'unit': 'mile', 'rate': 0.20288},
        
        # Transport
        {'category': 'Transport', 'type': 'Taxi', 'unit': 'km', 'rate': 0.14861},
        {'category': 'Transport', 'type': 'Bus', 'unit': 'km', 'rate': 0.10846},
        {'category': 'Transport', 'type': 'Rail', 'unit': 'km', 'rate': 0.03546},
        {'category': 'Transport', 'type': 'Flight', 'unit': 'km', 'rate': 0.27257},
        
        # Energy
        {'category': 'Energy', 'type': 'Electricity', 'unit': 'kWh', 'rate': 0.20705},
        
        # Working
        {'category': 'Working', 'type': 'Office', 'unit': 'hour', 'rate': 0.03144},
        {'category': 'Working', 'type': 'Home', 'unit': 'hour', 'rate': 0.33378},
        
        # Accommodation
        {'category': 'Accommodation', 'type': 'Hotel-UK', 'unit': 'night', 'rate': 10.40000},
        {'category': 'Accommodation', 'type': 'Hotel-London', 'unit': 'night', 'rate': 11.50000},
        
        # Motorbike
        {'category': 'Motorbike', 'type': 'Average', 'unit': 'km', 'rate': 0.11367}
    ]
    
    # Create multiple examples for each category with different amounts
    training_data = []
    for item in data:
        # Generate different amounts based on typical usage ranges
        if item['unit'] == 'mile':
            amounts = np.linspace(1, 1000, 100)  # 1-1000 miles
        elif item['unit'] == 'km':
            amounts = np.linspace(1, 500, 100)   # 1-500 km
        elif item['unit'] == 'kWh':
            amounts = np.linspace(1, 1000, 100)  # 1-1000 kWh
        elif item['unit'] == 'hour':
            amounts = np.linspace(1, 24, 24)     # 1-24 hours
        elif item['unit'] == 'night':
            amounts = np.linspace(1, 30, 30)     # 1-30 nights
        
        for amount in amounts:
            training_data.append({
                'category': item['category'],
                'type': item['type'],
                'unit': item['unit'],
                'amount': amount,
                'rate': item['rate'],
                'emissions': amount * item['rate']  # Calculates actual emissions
            })
    
    return pd.DataFrame(training_data)

def train_model(df):
    """Train the ML model on the emissions data"""
    # Encodes categorical variables
    le_category = LabelEncoder()
    le_type = LabelEncoder()
    le_unit = LabelEncoder()
    
    # Fit and transform categorical columns
    df['category_encoded'] = le_category.fit_transform(df['category'])
    df['type_encoded'] = le_type.fit_transform(df['type'])
    df['unit_encoded'] = le_unit.fit_transform(df['unit'])
    
    # Prepares features (X) and target (y)
    X = df[['category_encoded', 'type_encoded', 'unit_encoded', 'amount', 'rate']]
    y = df['emissions']
    
    # Splits the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Trains model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Prints model performance
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"\nModel R² score (training): {train_score:.4f}")
    print(f"Model R² score (testing): {test_score:.4f}")
    
    return model, le_category, le_type, le_unit

def predict_emissions(model, le_category, le_type, le_unit, category, type_, amount):
    """Predict emissions using the trained model"""
    # Gets the unit based on category
    unit_mapping = {
        'Car': 'mile',
        'Transport': 'km',
        'Energy': 'kWh',
        'Working': 'hour',
        'Accommodation': 'night',
        'Motorbike': 'km'
    }
    unit = unit_mapping[category]
    
    # Gets the rate for this category/type combination
    rates = {
        ('Car', 'Diesel'): 0.27334,
        ('Car', 'Petrol'): 0.26473,
        ('Car', 'Hybrid'): 0.20288,
        ('Transport', 'Taxi'): 0.14861,
        ('Transport', 'Bus'): 0.10846,
        ('Transport', 'Rail'): 0.03546,
        ('Transport', 'Flight'): 0.27257,
        ('Energy', 'Electricity'): 0.20705,
        ('Working', 'Office'): 0.03144,
        ('Working', 'Home'): 0.33378,
        ('Accommodation', 'Hotel-UK'): 10.40000,
        ('Accommodation', 'Hotel-London'): 11.50000,
        ('Motorbike', 'Average'): 0.11367
    }
    rate = rates[(category, type_)]
    
    # Encodes inputs
    category_encoded = le_category.transform([category])[0]
    type_encoded = le_type.transform([type_])[0]
    unit_encoded = le_unit.transform([unit])[0]
    
    # Makes prediction
    X_pred = [[category_encoded, type_encoded, unit_encoded, amount, rate]]
    prediction = model.predict(X_pred)[0]
    
    return prediction

if __name__ == "__main__":
    print("Creating training dataset from emissions factors...")
    df = create_training_dataset()
    
    print("Training ML model...")
    model, le_category, le_type, le_unit = train_model(df)
    
    while True:
        print("\nEmissions Calculator")
        print("-------------------")
        print("Categories: Car, Energy, Transport, Working, Accommodation, Motorbike")
        print("Types by category:")
        print("- Car: Diesel, Petrol, Hybrid")
        print("- Energy: Electricity")
        print("- Transport: Taxi, Bus, Rail, Flight")
        print("- Working: Office, Home")
        print("- Accommodation: Hotel-UK, Hotel-London")
        print("- Motorbike: Average")
        
        try:
            category = input("\nEnter category (or 'exit' to quit): ").strip()
            if category.lower() == 'exit':
                break
            
            category = category.capitalize()
            if category not in le_category.classes_:
                print(f"Invalid category. Please choose from: {', '.join(le_category.classes_)}")
                continue
            
            type_ = input("Enter type: ").strip()
            if category == 'Accommodation':
                type_ = type_.upper()
            else:
                type_ = type_.capitalize()
            
            if type_ not in le_type.classes_:
                print(f"Invalid type. Please check the types list above.")
                continue
            
            amount = float(input(f"Enter amount ({df[df['category'] == category]['unit'].iloc[0]}): "))
            
            # Calculates emissions
            ml_prediction = predict_emissions(model, le_category, le_type, le_unit, category, type_, amount)
            direct_calculation = amount * df[(df['category'] == category) & (df['type'] == type_)]['rate'].iloc[0]
            
            print(f"\nML model predicted emissions: {ml_prediction:.3f} kg CO2")
            print(f"Direct calculation emissions: {direct_calculation:.3f} kg CO2")
            print(f"Difference: {abs(ml_prediction - direct_calculation):.3f} kg CO2")
            
        except ValueError:
            print("Invalid input! Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")