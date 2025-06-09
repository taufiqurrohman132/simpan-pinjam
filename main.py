import customtkinter as ctk
from widget.sidebar import Sidebar
from views import dashboard, anggota, cicilan, simpanan, pinjaman, laporan, user
from auth import login_user, create_default_user, register_user
from database import conn

class KoperasiApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x600")
        self.title("Koperasi App")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.sidebar = Sidebar(self, self)
        self.sidebar.pack(side="left", fill="y")

        self.user = None

        create_default_user()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.show_login()

    def on_closing(self):
        try:
            self.destroy()
        except Exception as e:
            print(f"Gagal menutup dengan benar: {e}")

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ------------------- Halaman Login -------------------
    def show_login(self):
        self.clear_main()
        self.sidebar.pack_forget()  # sembunyikan sidebar saat login/register

        ctk.CTkLabel(self.main_frame, text="Login", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=20)

        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(pady=20)

        ctk.CTkLabel(frame, text="Username").grid(row=0, column=0, sticky="w", pady=5)
        username_entry = ctk.CTkEntry(frame)
        username_entry.grid(row=0, column=1, pady=5)

        ctk.CTkLabel(frame, text="Password").grid(row=1, column=0, sticky="w", pady=5)
        password_entry = ctk.CTkEntry(frame, show="*")
        password_entry.grid(row=1, column=1, pady=5)

        message_label = ctk.CTkLabel(self.main_frame, text="", text_color="red")
        message_label.pack()

        def do_login():
            username = username_entry.get()
            password = password_entry.get()
            user = login_user(username, password)
            if user:
                self.user = user
                self.sidebar.pack(side="left", fill="y")  # tampilkan sidebar setelah login
                self.show_dashboard()
            else:
                message_label.configure(text="Username atau password salah")

        login_btn = ctk.CTkButton(self.main_frame, text="Login", command=do_login)
        login_btn.pack(pady=10)

        ctk.CTkButton(self.main_frame, text="Daftar Nasabah Baru", command=self.show_register).pack(pady=10)

    # ------------------- Halaman Register -------------------
    def show_register(self):
        self.clear_main()
        self.sidebar.pack_forget()  # sembunyikan sidebar saat register

        ctk.CTkLabel(self.main_frame, text="Daftar Nasabah Baru", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(pady=10)

        labels = ["Nama Lengkap", "Username", "Password", "Telepon", "Alamat", "Email"]
        entries = {}

        for i, label in enumerate(labels):
            ctk.CTkLabel(frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            if label == "Password":
                entry = ctk.CTkEntry(frame, show="*")
            else:
                entry = ctk.CTkEntry(frame)
            entry.grid(row=i, column=1, pady=5)
            entries[label] = entry

        message_label = ctk.CTkLabel(self.main_frame, text="", text_color="red")
        message_label.pack()

        def do_register():
            nama = entries["Nama Lengkap"].get().strip()
            username = entries["Username"].get().strip()
            password = entries["Password"].get()
            telepon = entries["Telepon"].get().strip()
            alamat = entries["Alamat"].get().strip()
            email = entries["Email"].get().strip()

            if not (nama and username and password and telepon and alamat and email):
                message_label.configure(text="Semua field harus diisi")
                return

            success, msg = register_user(nama, username, password, telepon, alamat, email)
            if success:
                message_label.configure(text="Pendaftaran berhasil! Silakan login.", text_color="green")
            else:
                message_label.configure(text=msg, text_color="red")

        ctk.CTkButton(self.main_frame, text="Daftar", command=do_register).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Kembali ke Login", command=self.show_login).pack(pady=5)

    # ------------------- Halaman Dashboard -------------------
    def show_dashboard(self):
        if not self.user:
            self.show_login()
            return

        self.clear_main()
        self.sidebar.pack(side="left", fill="y")

        # Sesuaikan tampilan dashboard berdasarkan role
        role = self.user[4]
        if role == "admin":
            dashboard.show_dashboard(self)
        elif role == "kasir":
            dashboard.show_dashboard_kasir(self)  # Buat fungsi khusus kasir di modul dashboard.py
        elif role == "nasabah":
            dashboard.show_dashboard_nasabah(self)  # Buat fungsi khusus nasabah di modul dashboard.py
        else:
            ctk.CTkLabel(self.main_frame, text="Role tidak dikenal", font=ctk.CTkFont(size=20)).pack(pady=20)

    # ------------------- Halaman Kelola -------------------
    def show_anggota(self):
        self.clear_main()
        self.sidebar.pack(side="left", fill="y")
        anggota.show_anggota(self)

    def show_user(self):
        self.clear_main()
        self.sidebar.pack(side="left", fill="y")
        user.show_user_management(self)

    def show_cicilan(self):
        self.clear_main()
        self.sidebar.pack(side="left", fill="y")
        cicilan.show_cicilan(self)

    def show_pinjaman(self):
        self.clear_main()
        self.sidebar.pack(side="left", fill="y")
        pinjaman.show_pinjaman(self)

    def show_simpanan(self):
        self.clear_main()
        self.sidebar.pack(side="left", fill="y")
        simpanan.show_simpanan(self)

    def show_laporan(self):
        self.clear_main()
        self.sidebar.pack(side="left", fill="y")
        laporan.show_laporan(self)

    # ------------------- Logout -------------------
    def logout(self):
        self.user = None
        self.sidebar.pack_forget()
        self.show_login()


if __name__ == "__main__":
    app = KoperasiApp()
    app.mainloop()
    conn.close()
