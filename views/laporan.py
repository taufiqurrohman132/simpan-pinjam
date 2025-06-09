# views/laporan.py
import customtkinter as ctk

def show_laporan(app):
    app.clear_main()
    ctk.CTkLabel(app.main_frame, text="Halaman Laporan", font=ctk.CTkFont(size=20)).pack(pady=20)
