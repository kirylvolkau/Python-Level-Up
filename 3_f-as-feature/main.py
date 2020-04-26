from hashlib import sha256
from functools import wraps
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Response, Cookie, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

import csv
import pandas as pd

class PatientToCreate(BaseModel):
	name : str
	surname : str 

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
	tmp = PatientToCreate(name = patient.name.item(), surname = patient.surname.item())
	return PatientToReturn(id = id, patient = tmp)

def add_patient(patient : PatientToCreate):
	insert = [get_id(), patient.name, patient.surname]
	with open('storage.csv', 'a+') as storage:
		csv_writer = csv.writer(storage)
		csv_writer.writerow(insert)

def reset():
	with open('storage.csv', 'r') as fin:
		data = fin.read().splitlines(True)
	with open('storage.csv', 'w') as fout:
		fout.writelines(data[0])


def is_logged_in(func):
	@wraps(func)
	def inner(*args, **kwargs):
		request = kwargs['request']
		if 'session_token' in request.cookies and request.cookies['session_token'] == app.allowed_user_hash:
			return func(*args,**kwargs)
		else:
			raise HTTPException(401,'Not authorized.')
	return inner


LOGIN = 'trudnY'
PASS = 'PaC13Nt'

responses = dict()
responses[200] = JSONResponse(status_code=200, content={"message" : "OK"})
responses[204] =  Response(status_code=204)

app = FastAPI()
app.secret_key = 'Mizt14O3sE3AWCviiIkUuwqURvGEf2Tn'
app.allowed_user_hash = sha256(bytes(f"{LOGIN}{PASS}{app.secret_key}",encoding='utf8')).hexdigest()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
@is_logged_in
def welcome(request : Request):
	return templates.TemplateResponse(name="greetings.html",context={"request":request,"user" : LOGIN})

@app.post('/login')
def login(response: Response, credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
	if credentials.username == LOGIN and credentials.password == PASS:
		response.set_cookie(key='session_token',value=app.allowed_user_hash)
		response.status_code = 302
		response.headers['Location'] = '/welcome'
		return response
	else:
		raise HTTPException(401, 'Invalid username/password')

@app.post('/logout')
def logout(request : Request, response : Response):
	response.delete_cookie('session_token')
	response.status_code = 302
	response.headers['Location'] = '/'
	return response

@app.get('/patient')
@is_logged_in
def get_patients(request : Request):
	df = pd.read_csv('storage.csv')
	answer = dict()
	for index,row in df.iterrows():
		answer[row['id']] = {"name":row['name'],"surname":row['surname']}
	return answer

@app.post('/patient')
@is_logged_in
def create_patient(patient : PatientToCreate, request:Request, response : Response):
	add_patient(patient)
	response.status_code = 302
	response.headers['Location'] = f'/patient/{get_id()-1}'
	return response

@app.get('/patient/{id}')
@is_logged_in
def get_patient(id: int, request : Request):
	patient = find_patient(id)
	if patient:
		return patient.patient
	else:
		return responses[204]

@app.delete('/patient/{id}')
@is_logged_in
def delete_patient(id:int, request : Request):
	df = pd.read_csv('storage.csv')
	patient = df[df.id == id]
	if not patient.empty:
		df = df[df.id != id]
		reset()
		df.to_csv('storage.csv', index=False)
	return responses[200]

