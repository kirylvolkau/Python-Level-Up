import secrets
from functools import wraps
from hashlib import sha256
from pydantic import BaseModel
from requests import auth
from fastapi import FastAPI, HTTPException, status, Response, Cookie, Request
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse


class UserLogin(BaseModel):
	login: str
	password: str

def is_logged_in(f):
	@wraps(f)
	def wrapper(*args,**kwargs):
		request = kwargs["request"]
		session_token = Cookie(None)
		if "session_token" in request.cookies:
			session_token = request.cookies["session_token"]
		if session_token != app.allowed_user_hash:
			raise HTTPException(status_code=401, detail='Not authorized')
		return f(*args,**kwargs)
	return wrapper
			

app = FastAPI()
app.secret_key = "very constatn and random secret, best 64 characters"
app.allowed_user_hash = sha256(bytes(f"trudnYPaC13Nt{app.secret_key}",encoding='utf8')).hexdigest()

@app.get('/')
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}


@app.get('/welcome/')
@is_logged_in
def welcome(request: Request, session_token: str = Cookie(None)):
	return {"message": "Hello World during the coronavirus pandemic!"}

@app.post('/login/')
def login_user(request_model : UserLogin, response : Response):
	user_hash = sha256(bytes(f"{request_model.login}{request_model.password}{app.secret_key}",encoding='utf8')).hexdigest()
	print(user_hash)
	print(app.allowed_user_hash)
	# change to smth using normal encoding - decoding // user_hash = encode(request_model.login,request_model.password)
	if app.allowed_user_hash != user_hash:
		raise HTTPException(status_code=401,detail='Login failed.')
	response = RedirectResponse( url='/welcome', status_code=status.HTTP_302_FOUND)
	response.set_cookie(key="session_token", value=user_hash)
	return response

