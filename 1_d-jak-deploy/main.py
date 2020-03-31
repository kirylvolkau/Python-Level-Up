from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import json

class PatientToCreate(BaseModel):
	name : str
	surename : str #mistake in the task.

class PatientToReturn(BaseModel):
	id: int
	patient: PatientToCreate


app = FastAPI()
patients = list()
ID = 0

responses = dict()
responses[200] = JSONResponse(status_code=200, content={"message" : "OK"})
responses[204] =  JSONResponse(status_code=204, content={})

def add_patient(patient : PatientToCreate):
	global patients, ID
	patients[ID] = {"name" : patient.name, "surename" : patient.surename}	
	ID += 1

def find_patient(id : int):
	global patients
	if id in [p.id for p in patients]:
		return patients[id] 
	else:
		return None
	
#task 1 - working
@app.get('/')
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}

#task 2 - working
@app.get('/method')
def method_get():
	return {"method": "GET"}

@app.post('/method')
def method_post():
	return {"method": "POST"}

@app.delete('/method')
def method_delete():
	return {"method": "DELETE"}

@app.put('/method')
def method_put():
	return {"method" : "PUT"}

#task 3
@app.post('/patient')
def create_patient(patientToCreate: PatientToCreate):
	global ID, patients
	patients.append(PatientToReturn(id = ID, patient = patientToCreate))
	ID += 1
	return patients[ID-1]

#task 4
@app.get('/patient/{id}')
def get_patient(id: int):
	patient = find_patient(id)
	return patient.patient if patient else responses[204]

#additional functionality
@app.delete('/all')
def reset():
	global patients
	patients.clear()
	return responses[200]

@app.get('/all')
def all_patients():
	return patients

