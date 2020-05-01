import sqlite3

with sqlite3.connect('chinook.db') as connection:
    cursor = connection.cursor()
    tracks = cursor.execute("SELECT name FROM tracks").fetchall()
    print(len(tracks))
    print(tracks[:2])

with sqlite3.connect('chinook.db') as connection:
	cursor =  connection.cursor()
	tracks = cursor.execute(f"SELECT TrackId FROM tracks LIMIT 10 OFFSET ").fetchall()
	print(tracks)