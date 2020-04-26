from fastapi import FastAPI, HTTPException, Cookie, Response, Depends, Request

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
def welcome(request: Request):
	return {"message": "Hello World during the coronavirus pandemic!"}
