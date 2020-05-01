import sqlite3
import aiosqlite
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

class Composer(BaseModel):
	name: str

class Page(BaseModel):
	page: int
	per_page: int

@app.on_event('startup')
async def startup():
	app.db_connection = await aiosqlite.connect('chinook.db')

@app.on_event('shutdown')
async def shutdown():
	await app.db_connection.close()

@app.get('/tracks/')
async def get_tracks_page(page: Page = None):
	limit = 10 if page==None else page.per_page
	offset = 0 if page==None else page.page*page.per_page
	app.db_connection.row_factory = sqlite3.Row
	cursor = await app.db_connection.execute(f"SELECT * FROM tracks LIMIT {limit} OFFSET {offset}")
	tracks = await cursor.fetchall()
	return tracks

@app.get('/tracks/composers/')
async def get_tracks_of_composer(composer : Composer):
	cursor = await app.db_connection.execute(f"SELECT Name FROM tracks WHERE Composer = '{composer.name}'")
	tracks = await cursor.fetchall()
	if(len(tracks) == 0):
		raise HTTPException(status_code=404,detail="Composer was not found.")
	return tracks
