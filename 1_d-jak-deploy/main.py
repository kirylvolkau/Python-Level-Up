import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import csv

class PatientToCreate(BaseModel):
	name : str
	surename : str #mistake in the task.

class PatientToReturn(BaseModel):
	id: int
	patient: PatientToCreate

#get patient, create patient, 
def get_id():
	count = 0
	with open('storage.csv') as storage:
		reader = csv.reader(storage)
		count = len(list(reader))-1
	return count

def find_patient(id: int):
	df = pd.read_csv('storage.csv')
	patient = df[df.id == id]
	if patient.empty:
		return None
	tmp = PatientToCreate(name = patient.name.item(), surename = patient.surename.item())
	return PatientToReturn(id = id, patient = tmp)

def add_patient(patient : PatientToCreate):
	insert = [get_id(), patient.name, patient.surename]
	with open('storage.csv', 'a+', newline='\n') as storage:
		csv_writer = csv.writer(storage)
		csv_writer.writerow(insert)

app = FastAPI()

responses = dict()
responses[200] = JSONResponse(status_code=200, content={"message" : "OK"})
responses[204] =  JSONResponse(status_code=204, content={})
	
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
	add_patient(patientToCreate)
	return find_patient(get_id()-1)

#task 4
@app.get('/patient/{id}')
def get_patient(id: int):
	patient = find_patient(id)
	return patient.patient if patient else responses[204]

#additional functionality
@app.delete('/all')
def reset():
	with open('storage.csv', 'r') as fin:
		data = fin.read().splitlines(True)
	with open('storage.csv', 'w') as fout:
		fout.writelines(data[0])
	return responses[200]

@app.get('/all')
def all_patients():
	df = pd.read_csv('storage.csv')
	return df.T.to_dict()
	

