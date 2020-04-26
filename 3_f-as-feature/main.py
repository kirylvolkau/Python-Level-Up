from hashlib import sha256
from functools import wraps
from fastapi import FastAPI, HTTPException, Response, Cookie, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials


def is_logged_in(func):
	@wraps(func)
	def inner(*args, **kwargs):
		request = kwargs['request']
		print(request.cookies)
		if 'session_token' in request.cookies and request.cookies['session_token'] == app.allowed_user_hash:
			return func(*args,**kwargs)
		else:
			raise HTTPException(401,'Not authorized.')
	return inner


LOGIN = 'trudnY'
PASS = 'PaC13Nt'

app = FastAPI()
app.secret_key = 'Mizt14O3sE3AWCviiIkUuwqURvGEf2Tn'
app.allowed_user_hash = sha256(bytes(f"{LOGIN}{PASS}{app.secret_key}",encoding='utf8')).hexdigest()

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
@is_logged_in
def welcome(request : Request):
	return {"message": "Hello World during the coronavirus pandemic!"}

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


