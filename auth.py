import hashlib
from database import c, conn  # Pastikan kamu sudah punya koneksi dan cursor di database.py

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_default_user():
    try:
        c.execute("INSERT INTO user (nama, username, password, role) VALUES (?, ?, ?, ?)",
                  ("Admin", "admin", hash_password("admin123"), "admin"))
        conn.commit()
    except:
        # Abaikan error jika user sudah ada
        pass

def login_user(username, password):
    hashed = hash_password(password)
    c.execute("SELECT * FROM user WHERE username=? AND password=?", (username, hashed))
    return c.fetchone()

def register_user(nama, username, password, telepon, alamat, email):
    # Cek apakah username sudah ada
    c.execute("SELECT * FROM user WHERE username=?", (username,))
    if c.fetchone():
        return False, "Username sudah digunakan"
    
    hashed = hash_password(password)
    try:
        c.execute(
            "INSERT INTO user (nama, username, password, telepon, alamat, email, role) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (nama, username, hashed, telepon, alamat, email, "nasabah")  # role default nasabah
        )
        conn.commit()
        return True, "Pendaftaran berhasil"
    except Exception as e:
        return False, f"Terjadi kesalahan: {e}"
