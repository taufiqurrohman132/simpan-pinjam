import customtkinter as ctk
from widget.sidebar import Sidebar
from views import dashboard, anggota, cicilan, simpanan, pinjaman, laporan
from auth import login_user, create_default_user
from database import conn

class KoperasiApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x600")
        self.title("Koperasi App")

        # Frame utama tempat konten views ditampilkan
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Sidebar
        self.sidebar = Sidebar(self, self)
        self.sidebar.pack(side="left", fill="y")

        self.user = None

        create_default_user()

        # Start dengan dashboard (atau login dulu sesuai kebutuhan)
        # Misal langsung login dummy user buat test
        self.user = ("1", "Admin", "admin", "admin")  
        self.protocol("WM_DELETE_WINDOW", self.on_closing)# (id_user, nama, username, role)
        self.show_dashboard()
    def on_closing(self):
        try:
            self.destroy()
        except Exception as e:
            print(f"Gagal menutup dengan benar: {e}")

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        if self.user and self.user[3] == "admin":  # role check
            dashboard.show_dashboard(self)
        else:
            self.clear_main()
            ctk.CTkLabel(self.main_frame, text="Akses Ditolak. Hanya Admin.", font=ctk.CTkFont(size=20)).pack(pady=20)

    def show_anggota(self):
        if self.user and self.user[3] == "admin":
            anggota.show_anggota(self)
        else:
            self.clear_main()
            ctk.CTkLabel(self.main_frame, text="Akses Ditolak. Hanya Admin.", font=ctk.CTkFont(size=20)).pack(pady=20)
    def show_cicilan(self):
        if self.user and self.user[3] == "admin":
            cicilan.show_cicilan(self)
        else:
            self.clear_main()
            ctk.CTkLabel(self.main_frame, text="Akses Ditolak. Hanya Admin.", font=ctk.CTkFont(size=20)).pack(pady=20)
    def show_simpanan(self):
        if self.user and self.user[3] == "admin":
            simpanan.show_simpanan(self)
        else:
            self.clear_main()
            ctk.CTkLabel(self.main_frame, text="Akses Ditolak. Hanya Admin.", font=ctk.CTkFont(size=20)).pack(pady=20)
    def show_pinjaman(self):
        if self.user and self.user[3] == "admin":
            pinjaman.show_pinjaman(self)
        else:
            self.clear_main()
            ctk.CTkLabel(self.main_frame, text="Akses Ditolak. Hanya Admin.", font=ctk.CTkFont(size=20)).pack(pady=20)
    def show_laporan(self):
        if self.user and self.user[3] == "admin":
            laporan.show_laporan(self)
        else:
            self.clear_main()
            ctk.CTkLabel(self.main_frame, text="Akses Ditolak. Hanya Admin.", font=ctk.CTkFont(size=20)).pack(pady=20)

    def logout(self):
        # contoh sederhana: reset user lalu tampilkan dashboard kosong / login
        self.user = None
        self.clear_main()
        label = ctk.CTkLabel(self.main_frame, text="Anda sudah logout", font=ctk.CTkFont(size=20))
        label.pack(pady=50)

if __name__ == "__main__":
    app = KoperasiApp()
    app.mainloop()
    conn.close()
