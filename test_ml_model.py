import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

def calculate_emission(category, type_, amount):
    """Calculate direct emissions based on user input"""
    emission_rates = {
        ('Car', 'Diesel'): 0.27334,      # per mile
        ('Car', 'Petrol'): 0.26473,      # per mile
        ('Car', 'Hybrid'): 0.20288,      # per mile
        ('Energy', 'Electricity'): 0.20705,  # per kWh
        ('Transport', 'Taxi'): 0.14861,   # per passenger.km
        ('Transport', 'Bus'): 0.10846,    # per passenger.km
        ('Transport', 'Rail'): 0.03546,   # per passenger.km
        ('Transport', 'Flight'): 0.27257, # per passenger.km
        ('Working', 'Office'): 0.03144,   # per hour
        ('Working', 'Home'): 0.33378,     # per hour
        ('Accommodation', 'Hotel-UK'): 10.40000,    # per night
        ('Accommodation', 'Hotel-London'): 11.50000, # per night
        ('Motorbike', 'Average'): 0.11367,  # per km
    }
    return amount * emission_rates[(category, type_)]

def generate_historical_data(days=365):
    """Generate synthetic historical emission data with patterns"""
    dates = pd.date_range(end=datetime.now(), periods=days)
    
    data = []
    for date in dates:
        # Add seasonal patterns
        season_factor = 1 + 0.3 * np.sin(2 * np.pi * date.dayofyear / 365)
        
        # Add weekly patterns
        weekday_factor = 1.3 if date.weekday() < 5 else 0.7
        
        # Generate typical usage patterns
        car_miles = np.random.normal(30, 10) * weekday_factor * season_factor
        energy_kwh = np.random.normal(20, 5) * season_factor
        transport_km = np.random.normal(15, 5) * weekday_factor
        
        # Calculate emissions
        car_emissions = car_miles * 0.27334
        energy_emissions = energy_kwh * 0.20705
        transport_emissions = transport_km * 0.14861
        
        total_emissions = car_emissions + energy_emissions + transport_emissions
        
        data.append({
            'date': date,
            'day_of_week': date.dayofweek,
            'month': date.month,
            'season': (date.month % 12 + 3) // 3,
            'is_weekend': date.weekday() >= 5,
            'car_miles': car_miles,
            'energy_kwh': energy_kwh,
            'transport_km': transport_km,
            'total_emissions': total_emissions
        })
    
    return pd.DataFrame(data)

def train_prediction_model(df):
    """Train model to predict future emissions"""
    features = ['day_of_week', 'month', 'season', 'is_weekend']
    X = df[features]
    y = df['total_emissions']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model

def predict_future_emissions(model, days=7):
    """Predict emissions for next few days"""
    future_dates = pd.date_range(start=datetime.now(), periods=days)
    predictions = []
    
    for date in future_dates:
        features = {
            'day_of_week': date.dayofweek,
            'month': date.month,
            'season': (date.month % 12 + 3) // 3,
            'is_weekend': date.weekday() >= 5
        }
        
        X_pred = pd.DataFrame([features])
        prediction = model.predict(X_pred)[0]
        
        predictions.append({
            'date': date.strftime('%Y-%m-%d'),
            'day': date.strftime('%A'),
            'predicted_emissions': round(prediction, 2)
        })
    
    return predictions

if __name__ == "__main__":
    print("Loading emission prediction model...")
    historical_data = generate_historical_data()
    prediction_model = train_prediction_model(historical_data)
    
    while True:
        print("\nEmissions Calculator and Predictor")
        print("----------------------------------")
        print("1. Calculate current emissions")
        print("2. View emission predictions")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            print("\nCategories: Car, Energy, Transport, Working, Accommodation, Motorbike")
            print("Types by category:")
            print("- Car: Diesel, Petrol, Hybrid")
            print("- Energy: Electricity")
            print("- Transport: Taxi, Bus, Rail, Flight")
            print("- Working: Office, Home")
            print("- Accommodation: Hotel-UK, Hotel-London")
            print("- Motorbike: Average")
            
            try:
                category = input("\nEnter category: ").strip().capitalize()
                
                # Validate category
                valid_categories = ['Car', 'Energy', 'Transport', 'Working', 'Accommodation', 'Motorbike']
                if category not in valid_categories:
                    print(f"Invalid category. Please choose from: {', '.join(valid_categories)}")
                    continue
                
                type_ = input("Enter type: ").strip()
                if category == 'Accommodation':
                    type_ = type_.upper()
                else:
                    type_ = type_.capitalize()
                
                # Get amount based on category
                amount_prompt = {
                    'Car': "Enter miles driven: ",
                    'Energy': "Enter electricity used (kWh): ",
                    'Transport': "Enter distance (km): ",
                    'Working': "Enter hours: ",
                    'Accommodation': "Enter nights: ",
                    'Motorbike': "Enter distance (km): "
                }
                
                amount = float(input(amount_prompt[category]))
                
                # Calculate emissions
                emissions = calculate_emission(category, type_, amount)
                print(f"\nCalculated CO2 emissions: {emissions:.3f} kg")
                
            except ValueError:
                print("Invalid input! Please enter a valid number.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        
        elif choice == "2":
            predictions = predict_future_emissions(prediction_model)
            print("\nPredicted Emissions (Next 7 days):")
            for pred in predictions:
                print(f"{pred['day']} ({pred['date']}): {pred['predicted_emissions']:.2f} kg CO2")
            
            # Additional insights
            weekday_avg = historical_data[~historical_data['is_weekend']]['total_emissions'].mean()
            weekend_avg = historical_data[historical_data['is_weekend']]['total_emissions'].mean()
            print(f"\nTypical weekday emissions: {weekday_avg:.2f} kg CO2")
            print(f"Typical weekend emissions: {weekend_avg:.2f} kg CO2")
            
        elif choice == "3":
            print("\nExiting program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")