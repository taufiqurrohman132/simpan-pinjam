import customtkinter as ctk
import sqlite3
import hashlib
import datetime
from tkinter import messagebox

# Database setup
conn = sqlite3.connect("koperasi.db")
c = conn.cursor()

c.executescript('''
CREATE TABLE IF NOT EXISTS anggota (
    id_anggota INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    alamat TEXT,
    no_hp TEXT,
    tanggal_gabung DATE
);

CREATE TABLE IF NOT EXISTS user (
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT CHECK(role IN ('admin','pengurus'))
);
''')
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

try:
    c.execute("INSERT INTO user (nama, username, password, role) VALUES (?, ?, ?, ?)",
              ("Admin", "admin", hash_password("admin123"), "admin"))
    conn.commit()
except sqlite3.IntegrityError:
    pass

def login_user(username, password):
    hashed = hash_password(password)
    c.execute("SELECT * FROM user WHERE username=? AND password=?", (username, hashed))
    return c.fetchone()

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.configure(width=200)
        self.pack_propagate(False)

        # Sidebar header
        self.label_title = ctk.CTkLabel(self, text="Koperasi App", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(pady=20)

        # Buttons
        self.btn_dashboard = ctk.CTkButton(self, text="Dashboard", command=self.app.show_dashboard, corner_radius=10)
        self.btn_dashboard.pack(fill="x", padx=20, pady=(0, 10))

        self.btn_anggota = ctk.CTkButton(self, text="Kelola Anggota", command=self.app.show_anggota, corner_radius=10)
        self.btn_anggota.pack(fill="x", padx=20, pady=(0, 10))

        self.btn_logout = ctk.CTkButton(self, text="Logout", command=self.app.logout, fg_color="#d9534f", hover_color="#c9302c", corner_radius=10)
        self.btn_logout.pack(side="bottom", fill="x", padx=20, pady=20)

class KoperasiApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Window config
        self.title("Koperasi App - Modern UI")
        self.geometry("900x600")
        self.minsize(700, 500)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.user = None

        # Appearance & theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        # Container frames
        self.sidebar = Sidebar(self, self, fg_color="#2c3e50")
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = ctk.CTkFrame(self, fg_color="#34495e")
        self.main_frame.pack(side="right", expand=True, fill="both")

        # Start with login screen
        self.login_screen()

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_main()
        self.sidebar.pack_forget()  # Hide sidebar on login

        self.login_frame = ctk.CTkFrame(self.main_frame, fg_color="#34495e")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.login_frame, text="Login Koperasi", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 30))

        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username", width=300)
        self.username_entry.pack(pady=10)
        self.username_entry.focus()

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", width=300, show="*")
        self.password_entry.pack(pady=10)

        self.error_label = ctk.CTkLabel(self.login_frame, text="", text_color="#e74c3c")
        self.error_label.pack(pady=(0, 10))

        login_btn = ctk.CTkButton(self.login_frame, text="Login", width=300, command=self.do_login, corner_radius=15)
        login_btn.pack(pady=10)

    def do_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = login_user(username, password)
        if user:
            self.user = user
            self.sidebar.pack(side="left", fill="y")  # Show sidebar after login
            self.show_dashboard()
        else:
            self.error_label.configure(text="Username atau password salah.")

    def logout(self):
        self.user = None
        self.sidebar.pack_forget()
        self.login_screen()

    def show_dashboard(self):
        self.clear_main()
        ctk.CTkLabel(self.main_frame, text=f"Selamat datang, {self.user[1]}", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=30)

        info_frame = ctk.CTkFrame(self.main_frame, fg_color="#3b5360", corner_radius=15)
        info_frame.pack(pady=20, padx=40, fill="x")

        ctk.CTkLabel(info_frame, text="Menu:", font=ctk.CTkFont(size=20)).pack(anchor="w", pady=10, padx=10)

        btn_anggota = ctk.CTkButton(info_frame, text="Kelola Anggota", width=200, command=self.show_anggota, corner_radius=10)
        btn_anggota.pack(pady=10, padx=10, anchor="w")

    def show_anggota(self):
        self.clear_main()

        title = ctk.CTkLabel(self.main_frame, text="Form Tambah Anggota", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=(30, 20))

        form_frame = ctk.CTkFrame(self.main_frame, fg_color="#3b5360", corner_radius=15)
        form_frame.pack(pady=10, padx=50, fill="x")

        ctk.CTkLabel(form_frame, text="Nama").grid(row=0, column=0, pady=8, padx=10, sticky="w")
        self.nama_entry = ctk.CTkEntry(form_frame)
        self.nama_entry.grid(row=0, column=1, pady=8, padx=10, sticky="ew")

        ctk.CTkLabel(form_frame, text="Alamat").grid(row=1, column=0, pady=8, padx=10, sticky="w")
        self.alamat_entry = ctk.CTkEntry(form_frame)
        self.alamat_entry.grid(row=1, column=1, pady=8, padx=10, sticky="ew")

        ctk.CTkLabel(form_frame, text="No HP").grid(row=2, column=0, pady=8, padx=10, sticky="w")
        self.nohp_entry = ctk.CTkEntry(form_frame)
        self.nohp_entry.grid(row=2, column=1, pady=8, padx=10, sticky="ew")

        form_frame.grid_columnconfigure(1, weight=1)

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="#34495e")
        btn_frame.pack(pady=20)

        simpan_btn = ctk.CTkButton(btn_frame, text="Simpan", width=120, command=self.simpan_anggota, corner_radius=15)
        simpan_btn.grid(row=0, column=0, padx=10)

        kembali_btn = ctk.CTkButton(btn_frame, text="Kembali", width=120, command=self.show_dashboard, corner_radius=15)
        kembali_btn.grid(row=0, column=1, padx=10)

    def simpan_anggota(self):
        nama = self.nama_entry.get().strip()
        alamat = self.alamat_entry.get().strip()
        no_hp = self.nohp_entry.get().strip()

        if not nama or not alamat or not no_hp:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        c.execute("INSERT INTO anggota (nama, alamat, no_hp, tanggal_gabung) VALUES (?, ?, ?, ?)",
                  (nama, alamat, no_hp, datetime.date.today()))
        conn.commit()

        messagebox.showinfo("Sukses", "Anggota berhasil ditambahkan.")
        self.show_dashboard()

    def on_close(self):
        conn.close()
        self.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")
    app = KoperasiApp()
    app.mainloop()

