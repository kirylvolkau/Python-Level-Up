import sqlite3 
from functools import wraps
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import StarletteHTTPException as HTTP
from pydantic import BaseModel
import fastapi.exceptions as exceptions

class Album(BaseModel):
	title: str
	artist_id: int

class NotFoundException(HTTPException):
	def __init__(self, who : str):
		super().__init__(status_code=404)
		self.detail = {"error" : f"{who} not found.".capitalize()}

def artist_exists(func):
	@wraps(func)
	def wrapper(*args,**kwargs):
		album = kwargs['album']
		artist = app.db_connection.execute(f'SELECT name FROM artists WHERE artistid = "{album.artist_id}"').fetchall()
		if(len(artist)==0):
			raise NotFoundException("artist")
		else:
			return func(*args, **kwargs)
	return wrapper

def get_album_by_id(id : int):
	app.db_connection.row_factory = sqlite3.Row
	album = app.db_connection.execute(f'SELECT * FROM albums WHERE albumid="{id}"').fetchall()
	return album[0]

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
	app.db_connection.row_factory = lambda cursor,row: row[0]
	tracks = app.db_connection.execute(f'SELECT name FROM tracks WHERE composer = "{composer_name}" ORDER BY name').fetchall()
	if len(tracks)==0:
		raise NotFoundException("composer")
	return tracks

@app.post('/albums/', status_code=201)
@artist_exists
def create_new_album(album: Album):
	app.db_connection.row_factory = lambda cursor,row: row[0]
	album = app.db_connection.execute(
		f'''INSERT INTO albums (title, artistid) 
		VALUES ("{album.title}", "{album.artist_id}")'''
	).lastrowid
	app.db_connection.commit()
	return get_album_by_id(album)

@app.get('/albums/{album_id}')
def get_album(album_id : int):
	album = get_album_by_id(album_id)
	if len(album)==0:
		raise NotFoundException("album")
	return album



