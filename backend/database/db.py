"""SQLite persistence for the NexAgriTech MVP."""
import os, sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv('NEXAGRITECH_DB', os.getenv('FARMVEDA_DB', Path(__file__).resolve().parents[2] / 'farmveda.db')))

def connect():
    con=sqlite3.connect(DB_PATH)
    con.row_factory=sqlite3.Row
    con.execute('PRAGMA foreign_keys=ON')
    return con

def init_db():
    with connect() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS farmers(id INTEGER PRIMARY KEY, name TEXT NOT NULL, farm_name TEXT, phone TEXT, location TEXT, acres REAL DEFAULT 0, language TEXT DEFAULT 'en', created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS crops(id INTEGER PRIMARY KEY, farmer_id INTEGER, name TEXT NOT NULL, variety TEXT, acres REAL DEFAULT 0, stage TEXT DEFAULT 'Sowing', planted_on TEXT, notes TEXT DEFAULT '', FOREIGN KEY(farmer_id) REFERENCES farmers(id));
        CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY, farmer_id INTEGER, name TEXT NOT NULL, category TEXT DEFAULT 'Vegetables', price REAL NOT NULL, quantity REAL NOT NULL, unit TEXT DEFAULT 'kg', description TEXT DEFAULT '', harvest_date TEXT, practices TEXT DEFAULT '', certification TEXT DEFAULT 'farmer_declared', nutrition TEXT DEFAULT 'Nutrition data unavailable', emoji TEXT DEFAULT '🥬', active INTEGER DEFAULT 1, FOREIGN KEY(farmer_id) REFERENCES farmers(id));
        CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY, customer TEXT NOT NULL, phone TEXT DEFAULT '', address TEXT DEFAULT '', items_json TEXT NOT NULL, total REAL NOT NULL, status TEXT DEFAULT 'Placed', channel TEXT DEFAULT 'online', created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL, crop TEXT DEFAULT '', due_date TEXT, done INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS reviews(id INTEGER PRIMARY KEY, product_id INTEGER, customer TEXT, rating INTEGER, body TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS advice(id INTEGER PRIMARY KEY, question TEXT, answer TEXT, language TEXT, media_json TEXT DEFAULT '[]', created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS lessons(id INTEGER PRIMARY KEY, title TEXT, kind TEXT, crop TEXT, language TEXT, script TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS market_prices(id INTEGER PRIMARY KEY, crop TEXT, market TEXT, price REAL, change_pct REAL, source TEXT, observed_on TEXT);
        CREATE TABLE IF NOT EXISTS customers(id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE COLLATE NOCASE, phone TEXT DEFAULT '', address TEXT DEFAULT '', salt TEXT NOT NULL DEFAULT '', password_hash TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS auth_sessions(token_hash TEXT PRIMARY KEY, customer_id INTEGER NOT NULL, expires_at TEXT NOT NULL, FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE);
        CREATE TABLE IF NOT EXISTS advice_media(id TEXT PRIMARY KEY, filename TEXT NOT NULL, mime_type TEXT NOT NULL, byte_size INTEGER NOT NULL, question TEXT DEFAULT '', language TEXT DEFAULT 'en', created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        ''')
        product_columns={r['name'] for r in db.execute('PRAGMA table_info(products)')}
        if 'nutrition' not in product_columns:
            db.execute("ALTER TABLE products ADD COLUMN nutrition TEXT DEFAULT 'Nutrition data unavailable'")
        advice_columns={r['name'] for r in db.execute('PRAGMA table_info(advice)')}
        if 'media_json' not in advice_columns:
            db.execute("ALTER TABLE advice ADD COLUMN media_json TEXT DEFAULT '[]'")
        customer_columns={r['name'] for r in db.execute('PRAGMA table_info(customers)')}
        if 'salt' not in customer_columns:
            db.execute("ALTER TABLE customers ADD COLUMN salt TEXT NOT NULL DEFAULT ''")
        if not db.execute('SELECT 1 FROM farmers LIMIT 1').fetchone():
            db.execute('INSERT INTO farmers(name,farm_name,phone,location,acres,language) VALUES(?,?,?,?,?,?)',('Ravi Kumar','Swarna Farm','+91 98765 43210','Guntur, Andhra Pradesh',6.2,'te'))
            for name,variety,area,stage,planted in [('Tomato','Arka Rakshak',2,'Flowering','2026-09-25'),('Green chilli','Teja',1.5,'Vegetative','2026-10-12'),('Turmeric','Prathibha',1.7,'Rhizome growth','2026-08-02'),('Brinjal','Neelam',1,'Fruiting','2026-09-20')]:
                db.execute('INSERT INTO crops(farmer_id,name,variety,acres,stage,planted_on) VALUES(1,?,?,?,?,?)',(name,variety,area,stage,planted))
            products=[('Organic tomatoes','Vegetables',42,55,'Ripe tomatoes, harvested this morning.','Neem-based pest management, compost, drip irrigation.','18 kcal · 0.9g protein · 0.2g fat · 3.9g carbohydrates · 1.2g fiber','🍅'),('Green chilli','Vegetables',55,32,'Fresh Teja green chillies.','Farmyard manure and neem-based pest management.','40 kcal · 2g protein · 0.4g fat · 9g carbohydrates · 1.5g fiber','🌶️'),('Farm fresh brinjal','Vegetables',38,28,'Glossy Neelam brinjal.','Compost, crop rotation and hand weeding.','25 kcal · 1g protein · 0.2g fat · 6g carbohydrates · 3g fiber','🍆'),('Red onions','Vegetables',34,40,'Locally grown red onions.','Farmer-declared natural growing practices.','40 kcal · 1.1g protein · 0.1g fat · 9.3g carbohydrates · 1.7g fiber','🧅')]
            for n,cat,price,qty,desc,practice,nutri,emoji in products:
                db.execute('INSERT INTO products(farmer_id,name,category,price,quantity,description,practices,certification,harvest_date,nutrition,emoji) VALUES(1,?,?,?,?,?,?,?,?,?,?)',(n,cat,price,qty,desc,practice,'farmer_declared','2026-11-20',nutri,emoji))
            for title,crop,done in [('Check soil moisture','Tomato',0),('Apply neem spray','Turmeric',0),('Inspect drip lines','Green chilli',1)]: db.execute('INSERT INTO tasks(title,crop,due_date,done) VALUES(?,?,date(),?)',(title,crop,done))
            for crop,price,change in [('Tomato',32,8),('Green chilli',48,4),('Lady’s finger',36,-2),('Brinjal',28,6),('Turmeric',112,3)]: db.execute('INSERT INTO market_prices(crop,market,price,change_pct,source,observed_on) VALUES(?,?,?,?,?,date())',(crop,'Guntur',price,change,'Illustrative demo data'))

def fetch_all(sql,args=()):
    with connect() as db:return [dict(r) for r in db.execute(sql,args).fetchall()]
def fetch_one(sql,args=()):
    with connect() as db:
        r=db.execute(sql,args).fetchone();return dict(r) if r else None
