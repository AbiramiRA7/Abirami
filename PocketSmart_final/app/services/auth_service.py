from ..database import get_conn
from ..utils.security import hash_password, verify_password

def create_user(name: str, email: str, password: str) -> int:
    with get_conn() as conn:
        cur = conn.execute("INSERT INTO users(name,email,password_hash) VALUES(?,?,?)", (name.strip(), email.lower(), hash_password(password)))
        return int(cur.lastrowid)

def authenticate(email: str, password: str):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE email=?", (email.lower(),)).fetchone()
    if not row or not verify_password(password, row["password_hash"]):
        return None
    return row
