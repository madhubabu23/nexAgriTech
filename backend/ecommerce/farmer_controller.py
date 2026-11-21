from backend.database.db import fetch_one
def primary_farmer():return fetch_one('SELECT * FROM farmers ORDER BY id LIMIT 1')
