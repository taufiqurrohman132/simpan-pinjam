import customtkinter as ctk
from tkinter import messagebox
from database import conn  # koneksi SQLite

def show_user_management(app):
    app.clear_main()

    # FRAME UTAMA
    main_frame = ctk.CTkFrame(app.main_frame)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # JUDUL DAN TOMBOL TAMBAH
    header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 10))

    title = ctk.CTkLabel(header_frame, text="Manajemen User / Anggota", font=ctk.CTkFont(size=24, weight="bold"))
    title.pack(side="left")

    btn_add = ctk.CTkButton(header_frame, text="Tambah User / Anggota", command=lambda: open_form())
    btn_add.pack(side="right")

    # FRAME TABEL
    table_frame = ctk.CTkFrame(main_frame)
    table_frame.pack(fill="both", expand=True)

    form_window = None

    def load_data():
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Header tabel
        headers = ["ID", "Nama", "Username", "Role", "Aksi"]
        for col, text in enumerate(headers):
            lbl = ctk.CTkLabel(table_frame, text=text, font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

        try:
            cur = conn.cursor()
            cur.execute("SELECT id_user, nama, username, role FROM user ORDER BY id_user")
            rows = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data: {e}")
            return

        for i, row in enumerate(rows, start=1):
            # Data kolom
            for j, val in enumerate(row):
                ctk.CTkLabel(table_frame, text=str(val)).grid(row=i, column=j, padx=5, pady=5, sticky="w")

            # Kolom aksi (edit & hapus)
            action_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
            action_frame.grid(row=i, column=4, padx=5, pady=5, sticky="w")

            ctk.CTkButton(action_frame, text="Edit", width=50,
                          command=lambda uid=row[0]: open_form(uid)).pack(side="left", padx=(0, 5))

            ctk.CTkButton(action_frame, text="Hapus", width=60, fg_color="red", hover_color="#cc3333",
                          command=lambda uid=row[0]: delete_user(uid)).pack(side="left")

    def open_form(id_user=None):
        nonlocal form_window
        if form_window and form_window.winfo_exists():
            form_window.focus()
            return

        form_window = ctk.CTkToplevel(app)
        form_window.title("Tambah User / Anggota" if id_user is None else "Edit User / Anggota")
        form_window.geometry("400x380")
        form_window.grab_set()
        helper.center_window(form_window, 500, 400)

        container = ctk.CTkFrame(form_window)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Nama
        ctk.CTkLabel(container, text="Nama Lengkap:").pack(anchor="w", pady=(0, 5))
        ent_nama = ctk.CTkEntry(container)
        ent_nama.pack(fill="x", pady=(0, 10))

        # Username
        ctk.CTkLabel(container, text="Username:").pack(anchor="w", pady=(0, 5))
        ent_username = ctk.CTkEntry(container)
        ent_username.pack(fill="x", pady=(0, 10))

        # Password
        ctk.CTkLabel(container, text="Password:").pack(anchor="w", pady=(0, 5))
        ent_password = ctk.CTkEntry(container, show="*")
        ent_password.pack(fill="x", pady=(0, 10))

        # Role
        ctk.CTkLabel(container, text="Role:").pack(anchor="w", pady=(0, 5))
        role_var = ctk.StringVar(value="anggota")
        role_menu = ctk.CTkOptionMenu(container, values=["admin", "pengurus", "anggota"], variable=role_var)
        role_menu.pack(fill="x", pady=(0, 10))

        # Jika mode edit
        if id_user:
            try:
                cur = conn.cursor()
                cur.execute("SELECT nama, username, password, role FROM user WHERE id_user=?", (id_user,))
                user = cur.fetchone()
                if user:
                    ent_nama.insert(0, user[0])
                    ent_username.insert(0, user[1])
                    ent_password.insert(0, user[2])
                    role_var.set(user[3])
            except Exception as e:
                messagebox.showerror("Error", f"Gagal memuat data: {e}")

        def save_user():
            nama = ent_nama.get().strip()
            username = ent_username.get().strip()
            password = ent_password.get()
            role = role_var.get()

            if not nama or not username or not password:
                messagebox.showwarning("Validasi", "Semua field wajib diisi.")
                return

            try:
                cur = conn.cursor()
                if id_user is None:
                    cur.execute("INSERT INTO user (nama, username, password, role) VALUES (?, ?, ?, ?)",
                                (nama, username, password, role))
                else:
                    cur.execute("UPDATE user SET nama=?, username=?, password=?, role=? WHERE id_user=?",
                                (nama, username, password, role, id_user))
                conn.commit()
                messagebox.showinfo("Sukses", "Data berhasil disimpan.")
                form_window.destroy()
                load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan data: {e}")

        ctk.CTkButton(container, text="Simpan", command=save_user).pack(pady=10)

    def delete_user(id_user):
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus user ini?"):
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM user WHERE id_user=?", (id_user,))
                conn.commit()
                messagebox.showinfo("Sukses", "User berhasil dihapus.")
                load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus user: {e}")

    load_data()
