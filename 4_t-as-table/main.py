import sqlite3
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.on_event('startup')
def startup():
	app.db_connection = sqlite3.connect('chinook.db', check_same_thread=False)

@app.on_event('shutdown')
def shutdown():
	app.db_connection.close()

@app.get('/tracks/')
def get_tracks_page(page:int = 0, per_page:int = 10):
	app.db_connection.row_factory = sqlite3.Row
	tracks = app.db_connection.execute(f'SELECT * FROM tracks LIMIT {per_page} OFFSET {page*per_page}').fetchall()
	return tracks

@app.get('/tracks/composers/')
def get_composer_by_name(composer_name:str):
	app.db_connection.row_factory = lambda c,x: x[0]
	tracks = app.db_connection.execute(f'SELECT name FROM tracks WHERE composer = "{composer_name}" ORDER BY name').fetchall()
	if len(tracks)==0:
		raise HTTPException(404, detail="No such composer.")
	else:
		return tracks
