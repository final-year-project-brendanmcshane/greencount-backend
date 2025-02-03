import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression

def create_test_dataset():
    """Create test dataset with expanded emissions categories"""
    # Create more samples for better training
    samples_per_category = 100  # Increased from 20
    total_categories = 13
    num_samples = samples_per_category * total_categories
    
    categories = ['Car', 'Car', 'Car', 'Energy', 'Transport', 'Transport', 'Transport', 'Transport',
                 'Working', 'Working', 'Accommodation', 'Accommodation', 'Motorbike']
    types = ['Diesel', 'Petrol', 'Hybrid', 'Electricity', 'Taxi', 'Bus', 'Rail', 'Flight',
             'Office', 'Home', 'Hotel-UK', 'Hotel-London', 'Average']
    
    # Create more focused ranges for each category
    amounts = []
    for cat, type_ in zip(categories * samples_per_category, types * samples_per_category):
        if cat == 'Car':
            amounts.append(np.random.uniform(0, 500))  # Realistic mile range
        elif cat == 'Energy':
            amounts.append(np.random.uniform(0, 1000))  # Realistic kWh range
        elif cat == 'Transport':
            amounts.append(np.random.uniform(0, 300))  # Realistic km range
        elif cat == 'Working':
            amounts.append(np.random.uniform(0, 24))   # Hours in a day
        elif cat == 'Accommodation':
            amounts.append(np.random.uniform(1, 30))    # Nights in a month
        elif cat == 'Motorbike':
            amounts.append(np.random.uniform(0, 300))  # Realistic km range
    
    data = {
        'category': np.repeat(categories, samples_per_category),
        'type': np.repeat(types, samples_per_category),
        'amount': amounts
    }
    
    # Emission rates
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
    
    # Calculate emissions using direct multiplication
    data['emissions'] = [amount * emission_rates[(cat, type_)] 
                        for cat, type_, amount in zip(data['category'], data['type'], data['amount'])]
    
    return pd.DataFrame(data)

def train_model(df):
    """Train ML model"""
    # Encode categorical variables
    le_category = LabelEncoder()
    le_type = LabelEncoder()
    
    category_encoded = le_category.fit_transform(df['category'])
    type_encoded = le_type.fit_transform(df['type'])
    
    # Prepare features and target
    X = np.column_stack((category_encoded, type_encoded, df['amount']))
    y = df['emissions']
    
    # Split data with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=True
    )
    
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Print model performance metrics
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"\nModel R² score (training): {train_score:.4f}")
    print(f"Model R² score (testing): {test_score:.4f}")
    
    return model, le_category, le_type

def calculate_emission_direct(category, type_, amount):
    """Calculate emissions using direct multiplication"""
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

def predict_emissions_ml(model, le_category, le_type, category, type_, amount):
    """Predict emissions using ML model"""
    category_encoded = le_category.transform([category])[0]
    type_encoded = le_type.transform([type_])[0]
    prediction = model.predict([[category_encoded, type_encoded, amount]])
    return prediction[0]

if __name__ == "__main__":
    # Create dataset and train model
    print("Creating dataset and training ML model...")
    df = create_test_dataset()
    model, le_category, le_type = train_model(df)
    print("Model training complete!")
    
    # Test predictions
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
            
            # Validate category
            valid_categories = ['Car', 'Energy', 'Transport', 'Working', 'Accommodation', 'Motorbike']
            if category.capitalize() not in valid_categories:
                print(f"Invalid category. Please choose from: {', '.join(valid_categories)}")
                continue
                
            type_ = input("Enter type: ").strip()
            
            # Validate type based on category
            valid_types = {
                'Car': ['Diesel', 'Petrol', 'Hybrid'],
                'Energy': ['Electricity'],
                'Transport': ['Taxi', 'Bus', 'Rail', 'Flight'],
                'Working': ['Office', 'Home'],
                'Accommodation': ['Hotel-UK', 'Hotel-London'],
                'Motorbike': ['Average']
            }
            
            category = category.capitalize()
            
            # Special handling for hotel types
            if category == 'Accommodation':
                if type_.upper() == 'HOTEL-UK':
                    type_ = 'Hotel-UK'
                elif type_.upper() == 'HOTEL-LONDON':
                    type_ = 'Hotel-London'
            else:
                type_ = type_.capitalize()
            
            if type_ not in valid_types[category]:
                print(f"Invalid type for {category}. Please choose from: {', '.join(valid_types[category])}")
                continue
            
            # Custom prompts based on category
            if category.lower() == 'car':
                amount = float(input("Enter miles driven: "))
            elif category.lower() == 'energy':
                amount = float(input("Enter electricity used (kWh): "))
            elif category.lower() == 'transport':
                amount = float(input("Enter distance (km): "))
            elif category.lower() == 'working':
                amount = float(input("Enter hours: "))
            elif category.lower() == 'accommodation':
                amount = float(input("Enter nights: "))
            elif category.lower() == 'motorbike':
                amount = float(input("Enter distance (km): "))
            
            # Calculate emissions using both methods
            direct_emissions = calculate_emission_direct(category, type_, amount)
            ml_emissions = predict_emissions_ml(model, le_category, le_type, category, type_, amount)
            
            print(f"\nDirect calculation CO2 emissions: {direct_emissions:.3f} kg")
            print(f"ML model predicted CO2 emissions: {ml_emissions:.3f} kg")
            print(f"Difference: {abs(direct_emissions - ml_emissions):.3f} kg")
            
        except ValueError:
            print("Invalid input! Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")