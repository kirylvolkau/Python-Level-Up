from functools import wraps
from hashlib import sha256
from fastapi import FastAPI, HTTPException, status, Response, Cookie, Request, Depends
from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

def is_logged_in(f):
	@wraps(f)
	def wrapper(*args,**kwargs):
		request = kwargs["request"]
		session_token = Cookie(None)
		if "session_token" in request.cookies:
			session_token = request.cookies["session_token"]
		if session_token != app.allowed_hash:
			raise HTTPException(status_code=401, detail='Not authorized')
		return f(*args,**kwargs)
	return wrapper
			

app = FastAPI()
app.secret = "simple secret for the app"
app.allowed_hash = sha256(bytes(f"trudnYPaC13Nt{app.secret}", encoding="utf8")).hexdigest()
security = HTTPBasic()

@app.get('/')
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}


@app.get('/welcome/')
@is_logged_in
def welcome(request: Request, session_token: str = Cookie(None)):
	return {"message": "Hello World during the coronavirus pandemic!"}


@app.post('/login')
def user_login(credentials : HTTPBasicCredentials = Depends(security)):
	if credentials.username == "trudnY" and credentials.password == "PaC13Nt":
		response = RedirectResponse(url='/welcome')
		s_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret}", encoding='utf8')).hexdigest()
		response.set_cookie(key="session_token",value=s_token)
		return response
	else:
		raise HTTPException(status_code=401, detail="Bad login/password.")

@app.post('/logout/')
@is_logged_in
def user_logout(response : Response):
	response = RedirectResponse(url='/')
	response.delete_cookie(key="session_token",path='/')
	response.headers['Location'] = '/'
	return response
	
