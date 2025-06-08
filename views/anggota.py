import customtkinter as ctk
from tkinter import messagebox
import datetime
from database import c, conn

def show_anggota(app):
    app.clear_main()

    ctk.CTkLabel(app.main_frame, text="Form Tambah Anggota", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(30, 20))

    form = ctk.CTkFrame(app.main_frame, fg_color="#3b5360", corner_radius=15)
    form.pack(pady=10, padx=50, fill="x")

    fields = {}
    for i, label in enumerate(["Nama", "Alamat", "No HP"]):
        ctk.CTkLabel(form, text=label).grid(row=i, column=0, padx=10, pady=8, sticky="w")
        entry = ctk.CTkEntry(form)
        entry.grid(row=i, column=1, padx=10, pady=8, sticky="ew")
        fields[label.lower()] = entry

    form.grid_columnconfigure(1, weight=1)

    def simpan():
        nama, alamat, no_hp = fields["nama"].get(), fields["alamat"].get(), fields["no hp"].get()
        if not nama or not alamat or not no_hp:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return
        c.execute("INSERT INTO anggota (nama, alamat, no_hp, tanggal_gabung) VALUES (?, ?, ?, ?)",
                  (nama, alamat, no_hp, datetime.date.today()))
        conn.commit()
        messagebox.showinfo("Sukses", "Anggota berhasil ditambahkan.")
        app.show_dashboard()

    btn_frame = ctk.CTkFrame(app.main_frame, fg_color="#34495e")
    btn_frame.pack(pady=20)
    ctk.CTkButton(btn_frame, text="Simpan", width=120, command=simpan).grid(row=0, column=0, padx=10)
    ctk.CTkButton(btn_frame, text="Kembali", width=120, command=app.show_dashboard).grid(row=0, column=1, padx=10)
