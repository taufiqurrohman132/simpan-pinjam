import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import datetime
from database import c, conn

def show_cicilan(app):
    app.clear_main()

    ctk.CTkLabel(app.main_frame, text="Manajemen Cicilan", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(30, 10))

    container = ctk.CTkFrame(app.main_frame)
    container.pack(padx=20, pady=10, fill="both", expand=True)

    # === Form ===
    form_frame = ctk.CTkFrame(container, corner_radius=15, fg_color="#2c3e50")
    form_frame.pack(side="top", fill="x", pady=10)

    ctk.CTkLabel(form_frame, text="Form Tambah / Edit Cicilan", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, pady=10)

    fields = {}
    labels = ["ID Pinjaman", "Jumlah", "Tanggal Jatuh Tempo", "Tanggal Pembayaran", "Status"]
    for i, label in enumerate(labels):
        ctk.CTkLabel(form_frame, text=label).grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
        entry = ctk.CTkEntry(form_frame, width=250)
        entry.grid(row=i+1, column=1, padx=10, pady=5)
        fields[label.lower()] = entry

    selected_id = tk.StringVar()

    def simpan():
        data = [fields[l.lower()].get() for l in labels]
        if not all(data[:3]):  # Validasi wajib
            messagebox.showerror("Error", "Field ID Pinjaman, Jumlah dan Tanggal Jatuh Tempo wajib diisi.")
            return

        if selected_id.get():
            c.execute("""
                UPDATE cicilan 
                SET id_pinjaman=?, jumlah=?, tanggal_jatuh_tempo=?, tanggal_pembayaran=?, status=? 
                WHERE id_cicilan=?""", (*data, selected_id.get()))
            messagebox.showinfo("Sukses", "Data cicilan diperbarui.")
        else:
            c.execute("""
                INSERT INTO cicilan (id_pinjaman, jumlah, tanggal_jatuh_tempo, tanggal_pembayaran, status) 
                VALUES (?, ?, ?, ?, ?)""", data)
            messagebox.showinfo("Sukses", "Data cicilan ditambahkan.")
        conn.commit()
        reset_form()
        tampilkan_data()

    def reset_form():
        for f in fields.values():
            f.delete(0, tk.END)
        selected_id.set("")

    def hapus():
        if not selected_id.get():
            messagebox.showerror("Error", "Pilih cicilan yang akan dihapus.")
            return
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            c.execute("DELETE FROM cicilan WHERE id_cicilan=?", (selected_id.get(),))
            conn.commit()
            reset_form()
            tampilkan_data()

    btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    btn_frame.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

    ctk.CTkButton(btn_frame, text="Simpan", command=simpan, width=120).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Reset", command=reset_form, width=120).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="Hapus", command=hapus, fg_color="red", hover_color="#c0392b", width=120).pack(side="left", padx=5)

    # === Tabel ===
    table_frame = ctk.CTkFrame(container)
    table_frame.pack(fill="both", expand=True, pady=10)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#ecf0f1", foreground="black", rowheight=28, fieldbackground="#ecf0f1")
    style.map("Treeview", background=[("selected", "#3498db")])

    columns = ("ID", "ID Pinjaman", "Jumlah", "Jatuh Tempo", "Pembayaran", "Status")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w", width=130)

    tree.pack(fill="both", expand=True)

    def tampilkan_data():
        for row in tree.get_children():
            tree.delete(row)
        c.execute("""
            SELECT id_cicilan, id_pinjaman, jumlah, tanggal_jatuh_tempo, 
                   COALESCE(tanggal_pembayaran, '-'), COALESCE(status, '-') 
            FROM cicilan ORDER BY id_cicilan DESC""")
        for row in c.fetchall():
            tree.insert("", "end", values=row)

    def on_select(event):
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, "values")
        selected_id.set(values[0])
        fields["id pinjaman"].delete(0, tk.END)
        fields["jumlah"].delete(0, tk.END)
        fields["tanggal jatuh tempo"].delete(0, tk.END)
        fields["tanggal pembayaran"].delete(0, tk.END)
        fields["status"].delete(0, tk.END)

        fields["id pinjaman"].insert(0, values[1])
        fields["jumlah"].insert(0, values[2])
        fields["tanggal jatuh tempo"].insert(0, values[3])
        fields["tanggal pembayaran"].insert(0, values[4])
        fields["status"].insert(0, values[5])

    tree.bind("<<TreeviewSelect>>", on_select)
    tampilkan_data()
