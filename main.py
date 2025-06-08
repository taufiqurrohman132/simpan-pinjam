import customtkinter as ctk
from widget.sidebar import Sidebar
from views import dashboard, anggota
from auth import login_user, create_default_user
from database import conn

class KoperasiApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("900x600")
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
        self.user = ("id_user", "Admin")
        self.show_dashboard()

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main()
        dashboard.show_dashboard(self)

    def show_anggota(self):
        self.clear_main()
        anggota.show_anggota(self)

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
