import sys
import os
import pytest


import supabase
import supabase._sync.client as _sbmod

# Stub out a Supabase client so tests don’t hit the real backend
class DummyClient:
    def __init__(self, *args, **kwargs):
        # ignore url/key args
        self._last_op = None

    def table(self, name):
        # ignore table name
        return self

    def insert(self, data):
        self._last_op = 'insert'
        return self

    def select(self, *args, **kwargs):
        self._last_op = 'select'
        return self

    def execute(self):
        class Result:
            pass
        res = Result()
        # Return fake data for insert vs select operations
        if self._last_op == 'insert':
            res.data = [{'id': 1}]
        
        else:
            res.data = []
        return res

    
    @property
    def auth(self):
        class AuthStub:
            def get_user(self, token):
                
                class U: user = type('u', (), {'id': 'stub'})()
                return U()
            def sign_up(self, data): return {}
            def sign_in_with_password(self, data): 
                class Sess: access_token = 'x'; refresh_token = 'y'; expires_in = 0
                class U: id='u'; email='e'; role='r'
                return type('R', (), {'session': Sess(), 'user': U()})()
        return AuthStub()

# Monkey-patch both entrypoints so app.create_client() yields our DummyClient
_sbmod.create_client = DummyClient
supabase.create_client = DummyClient


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app


@pytest.fixture
def client():
    """Set up Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    """GET / should return welcome message."""
    r = client.get('/')
    assert r.status_code == 200
    assert r.json == {'message': 'Welcome to the GreenCount API!'}


def test_add_data(client):
    """POST /add should return a list with an 'id' key."""
    payload = {
        "Name": "Electricity",
        "Metric": "Usage",
        "Unit": "kWh",
        "Value": 500.0
    }
    r = client.post('/add', json=payload)
    assert r.status_code == 201
    assert isinstance(r.json, list)
    assert "id" in r.json[0]


def test_get_data(client):
    """GET /get should return a list."""
    r = client.get('/get')
    assert r.status_code == 200
    assert isinstance(r.json, list)
