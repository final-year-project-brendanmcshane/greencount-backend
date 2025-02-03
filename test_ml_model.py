import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression

def create_test_dataset():
    """Create test dataset with expanded emissions categories"""
    # Define the number of samples (must be divisible by number of categories)
    samples_per_category = 20
    total_categories = 13
    num_samples = samples_per_category * total_categories
    
    # Create repeating categories and types
    categories = ['Car', 'Car', 'Car', 'Energy', 'Transport', 'Transport', 'Transport', 'Transport',
                 'Working', 'Working', 'Accommodation', 'Accommodation', 'Motorbike']
    types = ['Diesel', 'Petrol', 'Hybrid', 'Electricity', 'Taxi', 'Bus', 'Rail', 'Flight',
             'Office', 'Home', 'Hotel-UK', 'Hotel-London', 'Average']
    
    # Create realistic ranges for each category
    amounts = []
    for cat, type_ in zip(categories * samples_per_category, types * samples_per_category):
        if cat == 'Car':
            amounts.append(np.random.uniform(1, 100))  # miles
        elif cat == 'Energy':
            amounts.append(np.random.uniform(1, 500))  # kWh
        elif cat == 'Transport':
            amounts.append(np.random.uniform(1, 100))  # km
        elif cat == 'Working':
            amounts.append(np.random.uniform(1, 12))   # hours
        elif cat == 'Accommodation':
            amounts.append(np.random.uniform(1, 7))    # nights
        elif cat == 'Motorbike':
            amounts.append(np.random.uniform(1, 100))  # km
    
    data = {
        'category': np.repeat(categories, samples_per_category),
        'type': np.repeat(types, samples_per_category),
        'amount': amounts
    }
    
    # Emission rates (by category and type)
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

def calculate_emission(category, type_, amount):
    """Calculate emissions directly without ML"""
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

if __name__ == "__main__":
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
            
            # Calculate emissions directly instead of using ML
            emissions = calculate_emission(category, type_, amount)
            print(f"\nCalculated CO2 emissions: {emissions:.3f} kg")
            
        except ValueError:
            print("Invalid input! Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")