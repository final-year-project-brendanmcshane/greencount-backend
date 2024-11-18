import sys
import os
import pytest
from flask import Flask

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Import your Flask app

@pytest.fixture
def client():
    """Fixture to set up the test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home route"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'message': 'Welcome to the GreenCount API!'}

def test_add_data(client):
    """Test adding data to the database"""
    payload = {
        "Name": "Electricity",
        "Metric": "Usage",
        "Unit": "kWh",
        "Value": 500.0
    }
    response = client.post('/add', json=payload)
    assert response.status_code == 201
    assert "id" in response.json[0]

def test_get_data(client):
    """Test fetching data from the database"""
    response = client.get('/get')
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Ensure it returns a list
