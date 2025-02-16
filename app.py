from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get Supabase URL and KEY from the environment
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

# Initialize Supabase client# Initialize Supabase client
supabase: Client = create_client(
    SUPABASE_URL, 
    os.getenv('SUPABASE_SERVICE_KEY')  # Changed from SUPABASE_KEY
)

# Conversion rates (ensure they are consistent)
CONVERSION_RATES = {
    'kwh_to_mwh': 0.001,  # Lowercase conversion key
    'liters_to_gallons': 0.264172,
    'gallons_to_liters': 3.78541,
    'mwh_to_kwh': 1000,
    'electricity_to_mwh': 0.001  # Explicit conversion for 'electricity' to 'mwh'
}

# Carbon intensity data (tons of CO2 per MWh for various energy sources)
CARBON_INTENSITY = {
    'coal': 0.9,  # 0.9 tons of CO2 per MWh
    'natural_gas': 0.4,  # 0.4 tons of CO2 per MWh
    'wind': 0,  # 0 tons of CO2 per MWh (renewable)
    'solar': 0,  # 0 tons of CO2 per MWh (renewable)
    'electricity': 0.5  # 0.5 tons of CO2 per MWh (example for grid electricity)
}
# Food intensity data
FOOD_INTENSITY = {
    'beef': 27,  # kg of CO2 per kg of beef
    'chicken': 6,  # kg of CO2 per kg of chicken
    'vegetables': 0.5,  # kg of CO2 per kg of vegetables
    'pork': 12,  # kg of CO2 per kg of pork
    'dairy': 2.5,  # kg of CO2 per kg of dairy
}

EMISSION_DATA = [
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


@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the GreenCount API!'})

@app.route('/convert', methods=['POST'])
def convert_data():
    data = request.get_json()
    print(f"Received payload: {data}")  # Log the received payload

    # Validate 'Metric'
    if 'Metric' not in data or not isinstance(data['Metric'], str) or data['Metric'].strip() == '':
        return jsonify({"error": "Invalid or missing 'Metric' field"}), 400

    # Validate 'Value'
    if 'Value' not in data or not isinstance(data['Value'], (int, float)) or data['Value'] <= 0:
        return jsonify({"error": "Invalid or missing 'Value' field"}), 400

    # Validate 'TargetUnit'
    if 'TargetUnit' not in data or not isinstance(data['TargetUnit'], str) or data['TargetUnit'].strip() == '':
        return jsonify({"error": "Invalid or missing 'TargetUnit' field"}), 400

    # Normalize and extract inputs
    metric = data['Metric'].strip().lower()  # Normalize to lowercase (THIS LINE WAS ADDED)
    value = data['Value']
    target_unit = data['TargetUnit'].strip().lower()  # Normalize to lowercase

    # Construct conversion key
    conversion_key = f"{metric}_to_{target_unit}"
    print(f"Generated conversion_key: {conversion_key}")

    # Lookup conversion rate
    conversion_rate = CONVERSION_RATES.get(conversion_key)
    if conversion_rate is None:
        print(f"Error: Conversion rate not found for key: {conversion_key}")
        return jsonify({"error": f"Unsupported conversion: {conversion_key}"}), 400

    # Perform conversion
    converted_value = value * conversion_rate
    print(f"Conversion successful. Original: {value}, Converted: {converted_value}")

    # Calculate CO2 emissions if the metric is energy consumption
    if metric in CARBON_INTENSITY:
        carbon_intensity = CARBON_INTENSITY[metric]
        emissions = value * carbon_intensity  # Calculate CO2 emissions in tons
        print(f"Calculated emissions: {emissions} tons of CO2")
    else:
        emissions = None

    return jsonify({
        "Metric": data['Metric'],
        "OriginalValue": value,
        "ConvertedValue": converted_value,
        "TargetUnit": data['TargetUnit'],
        "Emissions": emissions
    }), 200


@app.route('/add', methods=['POST'])
def add_data():
    data = request.get_json()
    
    # Validate fields
    if 'Metric' not in data or not isinstance(data['Metric'], str) or data['Metric'].strip() == '':
        return jsonify({"error": "Invalid or missing 'Metric' field. It should be a non-empty string."}), 400
    if 'Unit' not in data or not isinstance(data['Unit'], str) or data['Unit'].strip() == '':
        return jsonify({"error": "Invalid or missing 'Unit' field. It should be a non-empty string."}), 400
    if 'Value' not in data or not isinstance(data['Value'], (int, float)):
        return jsonify({"error": "Invalid or missing 'Value' field. It should be a number."}), 400
    
    # Insert data
    response = supabase.table('test_table').insert(data).execute()
    return jsonify(response.data), 201

@app.route('/get', methods=['GET'])
def get_data():
    response = supabase.table('test_table').select('*').execute()
    return jsonify(response.data), 200

@app.route('/summarize', methods=['GET'])
def summarize_data():
    metric = request.args.get('metric')
    if not metric:
        return jsonify({"error": "Metric parameter is required"}), 400
    
    response = supabase.table('test_table').select('*').execute()
    records = response.data
    
    # Filter and summarize
    filtered = [record for record in records if record['Metric'].lower() == metric.lower()]
    total = sum(record['Value'] for record in filtered)
    count = len(filtered)
    average = total / count if count > 0 else 0

    return jsonify({
        "metric": metric,
        "total": total,
        "average": average,
        "count": count
    }), 200

@app.route('/food-impact', methods=['POST'])
def food_impact():
    data = request.get_json()
    print(f"Received payload: {data}")

    # Validate 'Food Item'
    if 'FoodItem' not in data or not isinstance(data['FoodItem'], str) or data['FoodItem'].strip() == '':
        return jsonify({"error": "Invalid or missing 'FoodItem' field"}), 400

    # Validate 'Weight'
    if 'Weight' not in data or not isinstance(data['Weight'], (int, float)) or data['Weight'] <= 0:
        return jsonify({"error": "Invalid or missing 'Weight' field"}), 400

    # Normalize food item input
    food_item = data['FoodItem'].strip().lower()  # Normalize to lowercase
    weight = data['Weight']

    # Lookup food impact
    food_impact = FOOD_INTENSITY.get(food_item)
    if food_impact is None:
        return jsonify({"error": f"Unsupported food item: {food_item}"}), 400

    # Calculate CO2 emissions
    emissions = weight * food_impact  # CO2 emissions in kg
    print(f"Calculated emissions: {emissions} kg of CO2")

    return jsonify({
        "FoodItem": data['FoodItem'],
        "Weight": weight,
        "Emissions": emissions
    }), 200

@app.route('/model-info', methods=['GET'])
def model_info():
    return jsonify({
        "model_name": "Carbon Emission Predictor",
        "algorithm": "Linear Regression",
        "status": "Model training not yet implemented",
    }), 200


@app.route('/add-user-emission', methods=['POST'])
def add_user_emission():
    data = request.get_json()
    print("1. Received data:", data)
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "No or invalid authorization header"}), 401

    try:
        user = supabase.auth.get_user(auth_header.split(' ')[1])
        user_id = user.user.id

        # Get emission rate from EMISSION_DATA
        emission_info = next(
            (item for item in EMISSION_DATA 
             if item['category'] == data['category'] and item['type'] == data['type']),
            None
        )
        print("2. Found emission_info:", emission_info)

        if not emission_info:
            return jsonify({"error": "Invalid category/type combination"}), 400

        # Calculate emissions using rate
        calculated_emissions = data['value'] * emission_info['rate']
        print("3. Calculated emissions:", calculated_emissions)

        record = {
            'user_id': user_id,
            'category': data['category'],
            'type': data['type'],
            'value': data['value'],
            'unit': emission_info['unit'],
            'emissions': calculated_emissions
        }
        print("4. Final record:", record)

        response = supabase.table('user_emissions_v2').insert(record).execute()
        return jsonify(response.data), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 400


@app.route('/get-user-emissions', methods=['GET'])
def get_user_emissions():
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "No or invalid authorization header"}), 401

    try:
        # Validate token and get user ID
        user = supabase.auth.get_user(auth_header.split(' ')[1])  
        user_id = user.user.id

        # Fetch emissions for this user
        response = supabase.table('user_emissions_v2')\
            .select('*')\
            .eq('user_id', user_id)\
            .execute()

        return jsonify(response.data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 401


@app.route('/test-emission', methods=['POST'])
def test_emission():
    data = request.get_json()
    try:
        response = supabase.table('user_emissions').insert({
            'user_id': '12345', # Temporary test ID
            'metric': data.get('Metric'),
            'unit': data.get('Unit'), 
            'value': data.get('Value')
        }).execute()
        print("Inserted data:", response.data)
        return jsonify({"success": True, "data": response.data})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)})


import uuid  # Add this at the top with other imports

@app.route('/test-db', methods=['GET'])
def test_db():
    try:
        # Create a proper UUID
        test_user_id = str(uuid.uuid4())
        
        test_data = {
            'user_id': test_user_id,  # Using proper UUID
            'metric': 'TestMetric',
            'unit': 'TestUnit',
            'value': 100
        }
        
        # Try to insert
        insert_response = supabase.table('user_emissions').insert(test_data).execute()
        print("Insert response:", insert_response.data)
        
        # Try to fetch
        fetch_response = supabase.table('user_emissions').select("*").execute()
        print("Fetch response:", fetch_response.data)
        
        return jsonify({
            "message": "Database test successful",
            "inserted": insert_response.data,
            "fetched": fetch_response.data
        })
        
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)})


import re  # Import for email validation

@app.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    try:
        response = supabase.auth.sign_up({"email": email, "password": password})

        if 'user' in response:
            user_data = {
                "id": response.user.id,
                "email": response.user.email,
                "created_at": response.user.created_at
            }
        else:
            user_data = None

        return jsonify({
            "message": "Signup successful",
            "user": user_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


import json

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print("Received raw data:", request.data)  # Log raw request data
        print("Parsed JSON data:", data)  # Log parsed JSON

        if not data or 'email' not in data or 'password' not in data:
            print("Error: Missing email or password")
            return jsonify({"error": "Missing email or password"}), 400

        # Call Supabase authentication
        response = supabase.auth.sign_in_with_password({
            "email": data['email'],
            "password": data['password']
        })

        # Convert the response to JSON manually
        session_data = {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "expires_in": response.session.expires_in,
            "user": {
                "id": response.user.id,
                "email": response.user.email,
                "role": response.user.role
            }
        }

        print("Returning JSON response:", session_data)  # Debugging print

        return jsonify(session_data), 200  # Ensure JSON-serializable response

    except Exception as e:
        print("Exception occurred:", str(e))
        return jsonify({"error": str(e)}), 400




if __name__ == '__main__':
    app.run(debug=True)



