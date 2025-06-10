import customtkinter as ctk
from tkinter import messagebox
import datetime
import tkinter as tk
from tkinter import ttk
from database import c, conn

def show_anggota(app):
    if app.role not in ["admin", "pengurus"]:
        messagebox.showwarning("Akses Ditolak", "Anda tidak memiliki akses ke menu Anggota.")
        return 
    app.clear_main()

    ctk.CTkLabel(app.main_frame, text="Manajemen Anggota", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(30, 10))

    container = ctk.CTkFrame(app.main_frame)
    container.pack(padx=20, pady=10, fill="both", expand=True)

    # === Form Tambah/Update Anggota ===
    form_frame = ctk.CTkFrame(container, corner_radius=15, fg_color="#2c3e50")
    form_frame.pack(side="top", fill="x", pady=10)

    ctk.CTkLabel(form_frame, text="Form Tambah / Edit Anggota", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, pady=10)

    fields = {}
    for i, label in enumerate(["Nama", "Alamat", "No HP"]):
        ctk.CTkLabel(form_frame, text=label).grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
        entry = ctk.CTkEntry(form_frame, width=250)
        entry.grid(row=i+1, column=1, padx=10, pady=5)
        fields[label.lower()] = entry

    selected_id = tk.StringVar()  # Menyimpan ID anggota yang dipilih (untuk update)

    def simpan():
        nama, alamat, no_hp = fields["nama"].get(), fields["alamat"].get(), fields["no hp"].get()
        if not nama or not alamat or not no_hp:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        if selected_id.get():
            c.execute("UPDATE anggota SET nama=?, alamat=?, no_hp=? WHERE id=?", (nama, alamat, no_hp, selected_id.get()))
            messagebox.showinfo("Sukses", "Anggota berhasil diperbarui.")
        else:
            c.execute("INSERT INTO anggota (nama, alamat, no_hp, tanggal_gabung) VALUES (?, ?, ?, ?)",
                      (nama, alamat, no_hp, datetime.date.today()))
            messagebox.showinfo("Sukses", "Anggota berhasil ditambahkan.")
        conn.commit()
        reset_form()
        tampilkan_data()

    def reset_form():
        for f in fields.values():
            f.delete(0, tk.END)
        selected_id.set("")

    def hapus():
        if not selected_id.get():
            messagebox.showerror("Error", "Pilih anggota untuk dihapus.")
            return
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus anggota ini?"):
            c.execute("DELETE FROM anggota WHERE id=?", (selected_id.get(),))
            conn.commit()
            reset_form()
            tampilkan_data()

    button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    button_frame.grid(row=4, column=0, columnspan=2, pady=10)

    ctk.CTkButton(button_frame, text="Simpan", command=simpan, width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Reset", command=reset_form, width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Hapus", command=hapus, fg_color="red", hover_color="#c0392b", width=120).pack(side="left", padx=5)

    # === Tabel Daftar Anggota ===
    table_frame = ctk.CTkFrame(container)
    table_frame.pack(fill="both", expand=True, pady=10)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#ecf0f1", foreground="black", rowheight=30, fieldbackground="#ecf0f1")
    style.map("Treeview", background=[("selected", "#3498db")])

    tree = ttk.Treeview(table_frame, columns=("ID", "Nama", "Alamat", "No HP", "Tanggal Gabung"), show="headings", height=8)
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="w", width=140)

    tree.pack(fill="both", expand=True)

    def tampilkan_data():
        for row in tree.get_children():
            tree.delete(row)
        c.execute("SELECT id_anggota, nama, alamat, no_hp, tanggal_gabung FROM anggota ORDER BY id_anggota DESC")
        for row in c.fetchall():
            tree.insert("", "end", values=row)

    def on_select(event):
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, "values")
        selected_id.set(values[0])
        fields["nama"].delete(0, tk.END)
        fields["alamat"].delete(0, tk.END)
        fields["no hp"].delete(0, tk.END)

        fields["nama"].insert(0, values[1])
        fields["alamat"].insert(0, values[2])
        fields["no hp"].insert(0, values[3])

    tree.bind("<<TreeviewSelect>>", on_select)
    tampilkan_data()
