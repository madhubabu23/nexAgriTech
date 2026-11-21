from backend.database.db import fetch_all,fetch_one
def list_products(category:str|None=None):
    return fetch_all('SELECT p.*,f.name farmer,f.location FROM products p LEFT JOIN farmers f ON f.id=p.farmer_id WHERE p.active=1'+(' AND p.category=?' if category else '')+' ORDER BY p.id DESC',((category,) if category else ()))
def get_product(product_id:int):return fetch_one('SELECT * FROM products WHERE id=? AND active=1',(product_id,))
