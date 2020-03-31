from fastapi.testclient import TestClient
from main import app
import pytest 

client = TestClient(app)
test_ID = 0
test_patients = dict()

#task 1 test
def test_root():
	reponse = client.get('/')
	assert reponse.status_code == 200
	assert reponse.json() == {'message': 'Hello World during the coronavirus pandemic!'}

#task 2 test
@pytest.mark.parametrize('method', ["GET","POST","DELETE","PUT"])
def test_method(method):
	if method == "GET":
		response = client.get('/method')
	if method == "PUT":
		response = client.put('/method')
	if method == "DELETE":
		response = client.delete('/method')
	if method == "POST":
		response = client.post('/method')
	assert response.status_code == 200
	assert response.json() == {"method" :  method}

#task 3 test
@pytest.mark.parametrize('patientToCreate', [
	{'name' : 'Frank', 'surename' : 'Underwood'},
	{'name' : 'Grzegorzł', 'surename' : 'Brzęczyszczykiewićż'},
	{'name' : 'Кирилл', 'surename' : 'Волков'},
])
def test_patient_creation(patientToCreate):
	global test_ID, test_patients
	response = client.post('/patient', json = patientToCreate)
	assert response.status_code == 200
	assert response.json() == {'id' : test_ID, 'patient' : patientToCreate}
	test_patients[test_ID] = patientToCreate
	test_ID += 1

#task 4 test
def test_getting_patients():
	global test_ID, test_patients
	for id in range(test_ID-1):
		response = client.get('/patient/'+str(id))
		assert response.status_code == 200
		assert response.json() == test_patients[id]

	response = client.get('/patient/'+str(test_ID))
	assert response.status_code == 204
	assert response.json() == {}

#get all patients test
def test_all():
	global test_ID
	response = client.get('/all')
	assert test_ID == len(response.json())

#reset list
def test_reset():
	response_del = client.delete('/all')
	response_get = client.get('/all')
	assert response_del.status_code == 200
	assert len(response_get.json()) == 0