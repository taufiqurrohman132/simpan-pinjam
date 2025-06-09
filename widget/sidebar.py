import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, fg_color="#2c3e50", **kwargs)

        self.app = app
        self.collapsed = False
        self.active_button = None
        self.configure(width=200)
        self.pack_propagate(False)

        self.menu_items = [
            {"text": "Dashboard", "icon": "🏠", "command": self.app.show_dashboard},
            {"text": "Kelola Anggota", "icon": "👥", "command": self.app.show_anggota},
            {"text": "Cicilan", "icon": "💳", "command": self.app.show_cicilan},
            {"text": "Pinjaman", "icon": "💰", "command": self.app.show_pinjaman},
            {"text": "Simpanan", "icon": "🏦", "command": self.app.show_simpanan},
            {"text": "Laporan", "icon": "📊", "command": self.app.show_laporan},
        ]

        # ======= Header / Judul =======
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", pady=(5, 0))

        self.title_label = ctk.CTkLabel(
            self.top_frame,
            text="Koperasi App",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        )
        self.title_label.pack(side="left", padx=10, pady=5)

        self.toggle_button = ctk.CTkButton(
            self.top_frame, text="☰", width=30, height=30, command=self.toggle_sidebar,
            fg_color="transparent", text_color="white", hover_color="#34495e"
        )
        self.toggle_button.pack(side="right", padx=10)

        # ======= Tombol Menu Utama =======
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.buttons = []
        for item in self.menu_items:
            btn = self.add_button(item["text"], item["icon"], item["command"])
            self.buttons.append(btn)

        # ======= Tombol Logout di bawah =======
        self.logout_button = ctk.CTkButton(
            self,
            text="🚪 Logout",
            command=self.app.logout,
            fg_color="#d9534f",
            hover_color="#c9302c",
            text_color="white",
            corner_radius=8,
            font=ctk.CTkFont(size=13),
            height=36
        )
        self.logout_button.pack(side="bottom", fill="x", padx=10, pady=10)

    def add_button(self, text, icon, command):
        def on_click():
            self.highlight_button(btn)
            command()

        btn = ctk.CTkButton(
            self.button_frame,
            text=f"{icon}  {text}",
            anchor="w",
            command=on_click,
            fg_color="transparent",
            text_color="white",
            hover_color="#34495e",
            corner_radius=6,
            font=ctk.CTkFont(size=13),
            height=36
        )
        btn.pack(fill="x", padx=10, pady=4)
        return btn

    def highlight_button(self, button):
        if self.active_button:
            self.active_button.configure(fg_color="transparent")
        button.configure(fg_color="#1abc9c")  # tombol aktif warna hijau
        self.active_button = button

    def toggle_sidebar(self):
        self.collapsed = not self.collapsed
        new_width = 60 if self.collapsed else 200
        self.configure(width=new_width)

        if self.collapsed:
            self.title_label.pack_forget()
            for btn, item in zip(self.buttons, self.menu_items):
                btn.configure(text=item["icon"], anchor="center", font=ctk.CTkFont(size=16))
            self.logout_button.configure(text="🚪")
        else:
            self.title_label.pack(side="left", padx=10, pady=5)
            for btn, item in zip(self.buttons, self.menu_items):
                btn.configure(text=f"{item['icon']}  {item['text']}", anchor="w", font=ctk.CTkFont(size=13))
            self.logout_button.configure(text="🚪 Logout")
