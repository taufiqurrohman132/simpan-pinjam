import hashlib
import sqlite3

# Koneksi ke database
conn = sqlite3.connect("koperasi.db")
c = conn.cursor()

# Fungsi hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Membuat user admin default
def create_default_user():
    try:
        c.execute("SELECT * FROM user WHERE username=?", ("admin",))
        if not c.fetchone():
            c.execute("INSERT INTO user (nama, username, password, role) VALUES (?, ?, ?, ?)",
                      ("Admin", "admin", hash_password("admin123"), "admin"))
            conn.commit()
    except Exception as e:
        print(f"Error create_default_user: {e}")

# Fungsi login
def login_user(username, password):
    hashed = hash_password(password)
    c.execute("SELECT * FROM user WHERE username=? AND password=?", (username, hashed))
    return c.fetchone()

# Fungsi pendaftaran khusus anggota
def register_anggota(nama, username, password, telepon, alamat):
    # Cek apakah username sudah digunakan
    c.execute("SELECT * FROM user WHERE username=?", (username,))
    if c.fetchone():
        return False, "Username sudah digunakan"

    hashed = hash_password(password)
    try:
        # Simpan ke tabel user (dengan role nasabah)
        c.execute(
            "INSERT INTO user (nama, username, password, role) VALUES (?, ?, ?, ?)",
            (nama, username, hashed, "nasabah")
        )
        user_id = c.lastrowid  # ID user yang baru ditambahkan

        # Simpan ke tabel anggota
        c.execute(
            "INSERT INTO anggota (nama, no_hp, alamat, id_user) VALUES (?, ?, ?, ?)",
            (nama, telepon, alamat, user_id)
        )

        conn.commit()
        return True, "Pendaftaran anggota berhasil"
    except Exception as e:
        return False, f"Terjadi kesalahan saat mendaftar: {e}"

# -------------------------
# Hak akses berdasarkan role
# -------------------------
ROLE_PERMISSIONS = {
    "admin": ["dashboard", "anggota", "simpanan", "pinjaman", "cicilan", "laporan", "user"],
    "kasir": ["dashboard", "simpanan", "pinjaman", "cicilan"],
    "nasabah": ["dashboard", "simpanan_pribadi", "pinjaman_pribadi"]
}

def get_allowed_pages(role):
    """Mengembalikan daftar halaman/menu yang bisa diakses berdasarkan role"""
    return ROLE_PERMISSIONS.get(role, [])
