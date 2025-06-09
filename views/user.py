import customtkinter as ctk
from tkinter import messagebox
from database import conn  # koneksi global

def show_user_management(app):
    app.clear_main()

    frame = ctk.CTkFrame(app.main_frame)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    title = ctk.CTkLabel(frame, text="Kelola Data User/Admin", font=ctk.CTkFont(size=24, weight="bold"))
    title.pack(pady=(0,15))

    table_frame = ctk.CTkFrame(frame)
    table_frame.pack(fill="both", expand=True)

    def load_data():
        for widget in table_frame.winfo_children():
            widget.destroy()

        headers = ["ID", "Nama", "Username", "Password", "Role", "Aksi"]
        for col, text in enumerate(headers):
            lbl = ctk.CTkLabel(table_frame, text=text, font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=0, column=col, padx=5, pady=5, sticky="w")

        try:
            cur = conn.cursor()
            cur.execute("SELECT user_id, nama, username, password, role FROM users ORDER BY user_id")
            rows = cur.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data: {e}")
            rows = []

        for i, row in enumerate(rows, start=1):
            for j, val in enumerate(row):
                lbl = ctk.CTkLabel(table_frame, text=str(val))
                lbl.grid(row=i, column=j, padx=5, pady=5, sticky="w")

            btn_edit = ctk.CTkButton(table_frame, text="Edit", width=50,
                                     command=lambda uid=row[0]: open_form(uid))
            btn_edit.grid(row=i, column=5, padx=(5, 2), pady=5, sticky="w")

            btn_delete = ctk.CTkButton(table_frame, text="Hapus", width=60,
                                       fg_color="red",
                                       hover_color="#cc3333",
                                       command=lambda uid=row[0]: delete_user(uid))
            btn_delete.grid(row=i, column=5, padx=(60, 5), pady=5, sticky="w")

    form_window = None

    def open_form(user_id=None):
        nonlocal form_window
        if form_window is not None and form_window.winfo_exists():
            form_window.focus()
            return

        form_window = ctk.CTkToplevel(app)
        form_window.title("Tambah User" if user_id is None else "Edit User")
        form_window.geometry("400x350")
        form_window.grab_set()

        lbl_nama = ctk.CTkLabel(form_window, text="Nama:")
        lbl_nama.pack(pady=(20,5))
        ent_nama = ctk.CTkEntry(form_window, width=300)
        ent_nama.pack()

        lbl_username = ctk.CTkLabel(form_window, text="Username:")
        lbl_username.pack(pady=(15,5))
        ent_username = ctk.CTkEntry(form_window, width=300)
        ent_username.pack()

        lbl_password = ctk.CTkLabel(form_window, text="Password:")
        lbl_password.pack(pady=(15,5))
        ent_password = ctk.CTkEntry(form_window, width=300, show="*")
        ent_password.pack()

        lbl_role = ctk.CTkLabel(form_window, text="Role:")
        lbl_role.pack(pady=(15,5))
        role_var = ctk.StringVar(value="pengurus")
        role_dropdown = ctk.CTkOptionMenu(form_window, values=["admin", "pengurus"], variable=role_var)
        role_dropdown.pack()

        if user_id is not None:
            try:
                cur = conn.cursor()
                cur.execute("SELECT nama, username, password, role FROM users WHERE user_id=?", (user_id,))
                user = cur.fetchone()
                if user:
                    ent_nama.insert(0, user[0])
                    ent_username.insert(0, user[1])
                    ent_password.insert(0, user[2])
                    role_var.set(user[3])
            except Exception as e:
                messagebox.showerror("Error", f"Gagal load data user: {e}")

        def save():
            nama = ent_nama.get().strip()
            username = ent_username.get().strip()
            password = ent_password.get()
            role = role_var.get()

            if not nama or not username or not password:
                messagebox.showwarning("Validasi", "Nama, Username, dan Password wajib diisi.")
                return

            try:
                cur = conn.cursor()
                if user_id is None:
                    cur.execute("INSERT INTO users (nama, username, password, role) VALUES (?, ?, ?, ?)",
                                (nama, username, password, role))
                else:
                    cur.execute("UPDATE users SET nama=?, username=?, password=?, role=? WHERE user_id=?",
                                (nama, username, password, role, user_id))
                conn.commit()
                messagebox.showinfo("Sukses", "Data user berhasil disimpan.")
                form_window.destroy()
                load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal simpan data: {e}")

        btn_save = ctk.CTkButton(form_window, text="Simpan", command=save)
        btn_save.pack(pady=20)

    def delete_user(user_id):
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus user ini?"):
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM users WHERE user_id=?", (user_id,))
                conn.commit()
                messagebox.showinfo("Sukses", "User berhasil dihapus.")
                load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal hapus user: {e}")

    btn_add = ctk.CTkButton(frame, text="Tambah User Baru", command=lambda: open_form(None))
    btn_add.pack(pady=(0,10))

    load_data()
