import requests

# Test signup
signup_data = {
    "email": "test@example.com",
    "password": "password123"
}

response = requests.post('http://localhost:5000/auth/signup', json=signup_data)
print("Signup response:", response.json())