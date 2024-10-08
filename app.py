from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for the app

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the GreenCount API!'})

if __name__ == '__main__':
    app.run(debug=True)
