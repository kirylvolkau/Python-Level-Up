import sqlite3
import aiosqlite
from fastapi import FastAPI
from pydantic import BaseModel

class PageRequest(BaseModel):
	page: int = None
	per_page: int = None

class TrackResponse(BaseModel):
	TrackId: int
	Name : str
	AlbumId : int
	MediaTypeId : int
	GenreId : int
	Composed: str
	Milliseconds : int
	Bytes : int
	UnitPrice : float

app = FastAPI()

@app.on_event('startup')
async def startup():
	app.db_connection = await aiosqlite.connect('chinook.db')

@app.on_event('shutdown')
async def shutdown():
	await app.db_connection.close()

@app.get('/tracks')
async def get_tracks_page(page: int = 0, per_page: int = 10):
	app.db_connection.row_factory = sqlite3.Row
	cursor = await app.db_connection.execute(f"SELECT * FROM tracks LIMIT {per_page} OFFSET {per_page*page}")
	tracks = await cursor.fetchall()
	return tracks
