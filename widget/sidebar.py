import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.configure(width=200)
        self.pack_propagate(False)

        ctk.CTkLabel(self, text="Koperasi App", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        self.add_button("Dashboard", self.app.show_dashboard)
        self.add_button("Kelola Anggota", self.app.show_anggota)
        self.add_button("Logout", self.app.logout, color="#d9534f")

    def add_button(self, text, command, color=None):
        btn = ctk.CTkButton(self, text=text, command=command, corner_radius=10,
                            fg_color=color if color else None)
        btn.pack(fill="x", padx=20, pady=(0, 10))
