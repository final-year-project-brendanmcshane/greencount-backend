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

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the GreenCount API!'})

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
    filtered = [record for record in records if record['Metric'] == metric]
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
