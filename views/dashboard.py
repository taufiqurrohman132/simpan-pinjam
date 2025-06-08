import customtkinter as ctk

def show_dashboard(app):
    app.clear_main()
    ctk.CTkLabel(app.main_frame, text=f"Selamat datang, {app.user[1]}", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=30)
