import requests

signup_data = {
    "email": "mcshanebrendan@yahoo.com",  # Use a real email format
    "password": "Password123!" 
}

response = requests.post('http://localhost:5000/auth/signup', json=signup_data)
print("Signup response:", response.json())