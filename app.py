from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
import os

app = Flask(__name__)
CORS(app)

# Supabase URL and Key from your environment variables or hardcode for now
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Home route to verify API is working
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the GreenCount API!'})

# Route to fetch all data from the test_table
@app.route('/test-data', methods=['GET'])
def get_test_data():
    response = supabase.table('test_table').select('*').execute()
    data = response.data
    return jsonify(data)

# Route to insert data into the test_table
@app.route('/test-data', methods=['POST'])
def add_test_data():
    # Assuming you're sending JSON data like {"name": "Sample Name", "value": 100}
    data = request.get_json()
    response = supabase.table('test_table').insert(data).execute()
    return jsonify(response.data)

if __name__ == '__main__':
    app.run(debug=True)
