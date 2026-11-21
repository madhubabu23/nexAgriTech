"""NexAgriTech REST API. Run with: uvicorn backend.main:app --reload"""
import json, hashlib, secrets, hmac, re, uuid
from pathlib import Path
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Header, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.database.db import init_db, connect, fetch_all, fetch_one
from backend.database.models import FarmerIn,CropIn,ProductIn,TaskIn,OrderIn,AdviceIn,PriceIn,LessonIn,ReviewIn,CustomerRegisterIn,CustomerLoginIn
from backend.agents.farming_agent import answer as farming_answer
from backend.agents.pricing_agent import suggest_price
from backend.agents.video_agent import make_script
from backend.agents.nutrition_agent import lookup as nutrition_lookup
from backend.services.weather_service import current_weather
from backend.services.soil_service import soil_guidance
from backend.services.payment_service import create_payment
from backend.services.delivery_service import delivery_quote
from backend.analytics.sales_analysis import summarize

app=FastAPI(title='NexAgriTech API',version='1.0.0',description='Farmer tools, marketplace, educational content and market insights. Demo values are identified in responses.')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:3000','http://127.0.0.1:3000'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
UPLOAD_DIR=Path(__file__).resolve().parents[1]/'uploads'/'advisor'
MAX_UPLOAD=20*1024*1024
ALLOWED_MEDIA={'image/jpeg':'.jpg','image/png':'.png','image/webp':'.webp','image/heic':'.heic','video/mp4':'.mp4','video/webm':'.webm','video/quicktime':'.mov'}

def token_hash(token:str)->str:return hashlib.sha256(token.encode()).hexdigest()
def password_hash(password:str,salt:bytes)->bytes:return hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1)
def create_session(customer_id:int)->str:
    token=secrets.token_urlsafe(36);expires=(datetime.utcnow()+timedelta(days=30)).isoformat(timespec='seconds')
    with connect() as d:d.execute('INSERT INTO auth_sessions(token_hash,customer_id,expires_at) VALUES(?,?,?)',(token_hash(token),customer_id,expires))
    return token
def current_customer(authorization:str|None):
    if not authorization or not authorization.lower().startswith('bearer '):return None
    token=authorization.split(' ',1)[1].strip()
    return fetch_one('SELECT c.id,c.name,c.email,c.phone,c.address FROM auth_sessions s JOIN customers c ON c.id=s.customer_id WHERE s.token_hash=? AND s.expires_at>?',(token_hash(token),datetime.utcnow().isoformat(timespec='seconds')))

@app.on_event('startup')
def startup():init_db()
@app.get('/api/health')
def health():return {'ok':True,'database':'sqlite'}
@app.post('/api/auth/register',status_code=201)
def register_customer(x:CustomerRegisterIn):
    if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',x.email):raise HTTPException(422,'Enter a valid email address')
    salt=secrets.token_bytes(16);digest=password_hash(x.password,salt)
    try:
        with connect() as d:cid=d.execute('INSERT INTO customers(name,email,phone,address,salt,password_hash) VALUES(?,?,?,?,?,?)',(x.name.strip(),x.email.strip().lower(),x.phone,x.address,salt.hex(),digest.hex())).lastrowid
    except Exception as e:
        if 'UNIQUE' in str(e):raise HTTPException(409,'An account with this email already exists')
        raise
    return {'token':create_session(cid),'customer':fetch_one('SELECT id,name,email,phone,address FROM customers WHERE id=?',(cid,))}
@app.post('/api/auth/login')
def login_customer(x:CustomerLoginIn):
    c=fetch_one('SELECT * FROM customers WHERE email=? COLLATE NOCASE',(x.email.strip(),))
    if not c or not hmac.compare_digest(password_hash(x.password,bytes.fromhex(c['salt'])).hex(),c['password_hash']):raise HTTPException(401,'Email or password is incorrect')
    return {'token':create_session(c['id']),'customer':{k:c[k] for k in ('id','name','email','phone','address')}}
@app.get('/api/auth/me')
def customer_me(authorization:str|None=Header(None)):
    c=current_customer(authorization)
    if not c:raise HTTPException(401,'Customer login required')
    return c
@app.post('/api/auth/logout')
def customer_logout(authorization:str|None=Header(None)):
    if authorization and authorization.lower().startswith('bearer '):
        with connect() as d:d.execute('DELETE FROM auth_sessions WHERE token_hash=?',(token_hash(authorization.split(' ',1)[1].strip()),))
    return {'ok':True}
@app.get('/api/orders/mine')
def customer_orders(authorization:str|None=Header(None)):
    c=current_customer(authorization)
    if not c:raise HTTPException(401,'Customer login required')
    return fetch_all("SELECT * FROM orders WHERE customer=? AND channel LIKE 'online%' ORDER BY id DESC",(c['name'],))
@app.get('/api/state')
def state():
    return {'farmer':fetch_one('SELECT * FROM farmers ORDER BY id LIMIT 1'),'crops':fetch_all('SELECT * FROM crops ORDER BY id DESC'),'products':fetch_all('SELECT p.*,f.name farmer,f.location,f.farm_name FROM products p LEFT JOIN farmers f ON f.id=p.farmer_id WHERE p.active=1 ORDER BY p.id DESC'),'tasks':fetch_all('SELECT * FROM tasks ORDER BY done,due_date'),'orders':fetch_all('SELECT * FROM orders ORDER BY id DESC'),'prices':fetch_all('SELECT * FROM market_prices ORDER BY crop'),'advice':fetch_all('SELECT * FROM advice ORDER BY id DESC LIMIT 30'),'lessons':fetch_all('SELECT * FROM lessons ORDER BY id DESC')}
@app.put('/api/farmer')
def update_farmer(x:FarmerIn):
    existing=fetch_one('SELECT id FROM farmers ORDER BY id LIMIT 1')
    with connect() as d:
        if existing:d.execute('UPDATE farmers SET name=?,farm_name=?,phone=?,location=?,acres=?,language=? WHERE id=?',(x.name,x.farm_name,x.phone,x.location,x.acres,x.language,existing['id']));fid=existing['id']
        else:fid=d.execute('INSERT INTO farmers(name,farm_name,phone,location,acres,language) VALUES(?,?,?,?,?,?)',(x.name,x.farm_name,x.phone,x.location,x.acres,x.language)).lastrowid
    return {'ok':True,'id':fid}
@app.post('/api/crops',status_code=201)
def add_crop(x:CropIn):
    farmer=fetch_one('SELECT id FROM farmers ORDER BY id LIMIT 1')
    if not farmer:raise HTTPException(400,'Create a farm profile first')
    with connect() as d:cid=d.execute('INSERT INTO crops(farmer_id,name,variety,acres,stage,planted_on,notes) VALUES(?,?,?,?,?,?,?)',(farmer['id'],x.name,x.variety,x.acres,x.stage,x.planted_on,x.notes)).lastrowid
    return {'id':cid,'ok':True}
@app.post('/api/tasks',status_code=201)
def add_task(x:TaskIn):
    with connect() as d:tid=d.execute('INSERT INTO tasks(title,crop,due_date) VALUES(?,?,?)',(x.title,x.crop,x.due_date)).lastrowid
    return {'id':tid,'ok':True}
@app.patch('/api/tasks/{task_id}')
def task_done(task_id:int,done:bool):
    with connect() as d:d.execute('UPDATE tasks SET done=? WHERE id=?',(int(done),task_id))
    return {'ok':True}
@app.post('/api/products',status_code=201)
def add_product(x:ProductIn):
    farmer=fetch_one('SELECT id FROM farmers ORDER BY id LIMIT 1')
    if not farmer:raise HTTPException(400,'Create a farmer profile first')
    with connect() as d:pid=d.execute('INSERT INTO products(farmer_id,name,category,price,quantity,unit,description,harvest_date,practices,certification,nutrition,emoji) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(farmer['id'],x.name,x.category,x.price,x.quantity,x.unit,x.description,x.harvest_date,x.practices,x.certification,x.nutrition,x.emoji)).lastrowid
    return {'id':pid,'ok':True}
@app.get('/api/products/{product_id}')
def get_product(product_id:int):
    p=fetch_one('SELECT p.*,f.name farmer,f.location,f.farm_name FROM products p LEFT JOIN farmers f ON f.id=p.farmer_id WHERE p.id=? AND p.active=1',(product_id,))
    if not p:raise HTTPException(404,'Product not found')
    p['nutrition_info']=nutrition_lookup(p['name']);p['reviews']=fetch_all('SELECT customer,rating,body,created_at FROM reviews WHERE product_id=? ORDER BY id DESC',(product_id,));return p
@app.patch('/api/products/{product_id}')
def update_product(product_id:int,price:float|None=None,quantity:float|None=None,active:bool|None=None):
    fields={k:v for k,v in {'price':price,'quantity':quantity,'active':active}.items() if v is not None}
    if fields:
        with connect() as d:d.execute('UPDATE products SET '+','.join(f'{k}=?' for k in fields)+' WHERE id=?',(*[int(v) if k=='active' else v for k,v in fields.items()],product_id))
    return {'ok':True}
@app.post('/api/orders',status_code=201)
def checkout(x:OrderIn,authorization:str|None=Header(None)):
    customer=current_customer(authorization)
    if not customer:raise HTTPException(401,'Sign in as a customer before checkout')
    if not x.items:raise HTTPException(400,'Basket is empty')
    entries=[];total=0
    with connect() as d:
        for line in x.items:
            p=d.execute('SELECT * FROM products WHERE id=? AND active=1',(line.product_id,)).fetchone()
            if not p or line.quantity>p['quantity']:raise HTTPException(409,'Product unavailable or quantity exceeds stock')
            total+=line.quantity*p['price'];entries.append({'product_id':p['id'],'name':p['name'],'quantity':line.quantity,'unit':p['unit'],'price':p['price']})
        oid=d.execute('INSERT INTO orders(customer,phone,address,items_json,total,status,channel) VALUES(?,?,?,?,?,?,?)',(customer['name'],customer['phone'] or x.phone,customer['address'] or x.address,json.dumps(entries,ensure_ascii=False),total,'Placed','online · demo payment')).lastrowid
        for line in x.items:d.execute('UPDATE products SET quantity=quantity-? WHERE id=?',(line.quantity,line.product_id))
    return {'id':oid,'total':round(total,2),'payment':create_payment(total),'status':'Placed'}
@app.post('/api/offline-sales',status_code=201)
def offline_sale(product_id:int,quantity:float,customer:str='Farm-gate customer'):
    with connect() as d:
        p=d.execute('SELECT * FROM products WHERE id=? AND active=1',(product_id,)).fetchone()
        if not p or quantity<=0 or quantity>p['quantity']:raise HTTPException(400,'Quantity unavailable')
        items=[{'product_id':p['id'],'name':p['name'],'quantity':quantity,'unit':p['unit'],'price':p['price']}];total=quantity*p['price'];oid=d.execute('INSERT INTO orders(customer,items_json,total,status,channel) VALUES(?,?,?,?,?)',(customer,json.dumps(items),total,'Completed','farm-gate')).lastrowid;d.execute('UPDATE products SET quantity=quantity-? WHERE id=?',(quantity,product_id))
    return {'id':oid,'total':total,'ok':True}
@app.post('/api/reviews',status_code=201)
def add_review(product_id:int,x:ReviewIn):
    with connect() as d:rid=d.execute('INSERT INTO reviews(product_id,customer,rating,body) VALUES(?,?,?,?)',(product_id,x.customer,x.rating,x.body)).lastrowid
    return {'id':rid,'ok':True}
@app.post('/api/advice')
def get_advice(x:AdviceIn):
    from backend.services.multimodal_advisor import advise
    media=[m.model_dump() for m in x.media] if x.media_consent else []
    result=advise(x.question,x.language,media)
    with connect() as d:d.execute('INSERT INTO advice(question,answer,language,media_json) VALUES(?,?,?,?)',(x.question,result['answer'],x.language,json.dumps([m.get('name','attachment') for m in media])))
    return {**result,'disclaimer':'Educational guidance only. Confirm diagnoses and treatments with a local agriculture professional.'}
@app.post('/api/advice/media',status_code=201)
async def upload_advisor_media(files:list[UploadFile]=File(...),question:str=Form(''),language:str=Form('en'),media_consent:bool=Form(False)):
    if not files or len(files)>5:raise HTTPException(400,'Upload between 1 and 5 files')
    prepared=[]
    for item in files:
        mime=item.content_type or ''
        if mime not in ALLOWED_MEDIA:raise HTTPException(415,f'Unsupported media type: {mime or "unknown"}')
        raw=await item.read(MAX_UPLOAD+1)
        if len(raw)>MAX_UPLOAD:raise HTTPException(413,'Each photo or video must be 20 MB or smaller')
        import base64
        data_url='data:'+mime+';base64,'+base64.b64encode(raw).decode('ascii') if mime.startswith('image/') else None
        prepared.append((uuid.uuid4().hex+ALLOWED_MEDIA[mime],mime,raw,data_url))
    UPLOAD_DIR.mkdir(parents=True,exist_ok=True);saved=[]
    for filename,mime,raw,data_url in prepared:
        (UPLOAD_DIR/filename).write_bytes(raw);saved.append({'id':filename.split('.')[0],'filename':filename,'name':filename,'mime_type':mime,'byte_size':len(raw),'data_url':data_url,'analysis_available':bool(media_consent and data_url)})
    with connect() as d:
        for item in saved:d.execute('INSERT INTO advice_media(id,filename,mime_type,byte_size,question,language) VALUES(?,?,?,?,?,?)',(item['id'],item['filename'],item['mime_type'],item['byte_size'],question,language))
    from backend.services.multimodal_advisor import advise
    result=advise(question or 'Please inspect this crop and describe visible concerns and safe organic next steps.',language,saved if media_consent else [])
    with connect() as d:d.execute('INSERT INTO advice(question,answer,language,media_json) VALUES(?,?,?,?)',(question or 'Crop photo/video submitted',result['answer'],language,json.dumps([x['filename'] for x in saved])))
    return {'files':[{k:v for k,v in f.items() if k!='data_url'} for f in saved],**result,'analysis_available':result.get('media_analyzed',False),'message':result.get('note','Media stored.')}
@app.post('/api/pricing/suggest')
def price_suggestion(x:PriceIn):
    result=suggest_price({'seeds':x.seed,'fertilizer':x.fertilizer,'labor':x.labor,'water':x.water,'packaging':x.packaging,'transport':x.transport},x.quantity,x.profit)
    market=fetch_one('SELECT * FROM market_prices WHERE lower(crop)=lower(?) ORDER BY id DESC LIMIT 1',(x.crop,))
    return {**result,'market_observation':market,'note':'Cost-based suggestion. Market rows are illustrative demo data until a licensed feed is configured.'}
@app.get('/api/nutrition/{name}')
def nutrition(name:str):return nutrition_lookup(name)
@app.post('/api/lessons',status_code=201)
def create_lesson(x:LessonIn):
    script=make_script(x.crop,x.kind,x.language);title=x.title or f'{x.crop} {x.kind} guide'
    with connect() as d:lid=d.execute('INSERT INTO lessons(title,kind,crop,language,script) VALUES(?,?,?,?,?)',(title,x.kind,x.crop,x.language,script)).lastrowid
    return {'id':lid,'title':title,'kind':x.kind,'crop':x.crop,'language':x.language,'script':script,'rendered_video':False,'disclosure':'Storyboard and narration text only; no generated video footage is attached.'}
@app.get('/api/market/prices')
def market_prices():return {'items':fetch_all('SELECT * FROM market_prices ORDER BY crop'),'source':'Illustrative demo data','live':False}
@app.get('/api/analytics')
def analytics():return summarize(fetch_all('SELECT * FROM orders'),fetch_all('SELECT * FROM products WHERE active=1'))
@app.get('/api/weather')
def weather(location:str='Guntur'):return current_weather(location)
@app.get('/api/soil')
def soil(ph:float|None=None,organic_carbon:float|None=None):return soil_guidance(ph,organic_carbon)
@app.get('/api/delivery')
def delivery(location:str=''):return delivery_quote(location)
