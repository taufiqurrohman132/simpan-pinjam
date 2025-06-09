# views/pinjaman.py
import customtkinter as ctk

def show_pinjaman(app):
    app.clear_main()
    ctk.CTkLabel(app.main_frame, text="Halaman Pinjaman", font=ctk.CTkFont(size=20)).pack(pady=20)
