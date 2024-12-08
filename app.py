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

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
}

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
    metric = data['Metric'].strip().lower()  # Normalize to lowercase
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

if __name__ == '__main__':
    app.run(debug=True)
