"""Customer signup, login and bearer-session helpers for the MVP."""
import hashlib, hmac, secrets
from datetime import datetime, timedelta, timezone
from backend.database.db import connect, fetch_one

def hash_password(password:str)->str:
    salt=secrets.token_bytes(16)
    key=hashlib.pbkdf2_hmac('sha256',password.encode(),salt,310_000)
    return 'pbkdf2_sha256$310000$'+salt.hex()+'$'+key.hex()

def verify_password(password:str,stored:str)->bool:
    try:
        _,rounds,salt,key=stored.split('$')
        return hmac.compare_digest(hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt),int(rounds)).hex(),key)
    except (ValueError,TypeError):return False

def issue_session(customer_id:int)->str:
    token=secrets.token_urlsafe(32);digest=hashlib.sha256(token.encode()).hexdigest();expires=(datetime.now(timezone.utc)+timedelta(days=30)).isoformat()
    with connect() as db:db.execute('INSERT INTO customer_sessions(token_hash,customer_id,expires_at) VALUES(?,?,?)',(digest,customer_id,expires))
    return token

def customer_for_token(token:str|None):
    if not token:return None
    digest=hashlib.sha256(token.encode()).hexdigest()
    return fetch_one('SELECT c.id,c.name,c.email,c.phone,c.address FROM customer_sessions s JOIN customers c ON c.id=s.customer_id WHERE s.token_hash=? AND s.expires_at>?',(digest,datetime.now(timezone.utc).isoformat()))

def revoke_session(token:str|None):
    if token:
        with connect() as db:db.execute('DELETE FROM customer_sessions WHERE token_hash=?',(hashlib.sha256(token.encode()).hexdigest(),))
