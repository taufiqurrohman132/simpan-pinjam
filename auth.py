import hashlib
from database import c, conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_default_user():
    try:
        c.execute("INSERT INTO user (nama, username, password, role) VALUES (?, ?, ?, ?)",
                  ("Admin", "admin", hash_password("admin123"), "admin"))
        conn.commit()
    except:
        pass

def login_user(username, password):
    hashed = hash_password(password)
    c.execute("SELECT * FROM user WHERE username=? AND password=?", (username, hashed))
    return c.fetchone()
