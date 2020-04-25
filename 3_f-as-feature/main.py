from basicauth import encode, decode
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status, Response
from fastapi.responses import JSONResponse


class UserLogin(BaseModel):
	login: str
	password: str

app = FastAPI()
app.secret_key = "very constatn and random secret, best 64 characters"
app.allowed_user_hash = encode('trudnY','PaC13Nt') #later it should be stored in db next to username

@app.get('/')
@app.get('/welcome/')
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}

@app.post('/login/')
def login_user(request_model : UserLogin,response : Response, status_code=status.HTTP_200_OK):
	user_hash = encode(request_model.login,request_model.password)
	if app.allowed_user_hash == user_hash:
		response.set_cookie(key='session_token', value=user_hash)
	else:
		raise HTTPException(401)

