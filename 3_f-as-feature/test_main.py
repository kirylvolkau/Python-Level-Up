import pytest 
from main import app
from basicauth import encode, decode
from fastapi.testclient import TestClient


client = TestClient(app)
client.login_hash = encode('trudnY','PaC13Nt')

def test_root():
	reponse = client.get('/')
	assert reponse.status_code == 200
	assert reponse.json() == {'message': 'Hello World during the coronavirus pandemic!'}

def test_welcome():
	response = client.get('/welcome')
	assert response.status_code == 200
	assert response.json() == {'message': 'Hello World during the coronavirus pandemic!'}

def test_bad_login():
	request = {"login":"no","password":"no"}
	response = client.post('/login/',json=request)
	assert response.status_code==401

def test_correct_login():
	request = {'login':'trudnY','password':'PaC13Nt'}
	response = client.post(url='/login/', json=request)
	assert response.status_code == 200
	assert response.cookies.get('session_token') == f'"{client.login_hash}"'



