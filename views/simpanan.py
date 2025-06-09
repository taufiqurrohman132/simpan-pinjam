import customtkinter as ctk
from tkinter import messagebox
import datetime
import sqlite3

# Koneksi ke database
def get_connection():
    return sqlite3.connect("koperasi.db")

# Tampilan dan fungsi utama Simpanan
def show_simpanan(app):
    app.clear_main()

    def load_simpanan():
        tree.delete(*tree.get_children())
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.simpanan_id, a.nama, s.jenis_simpanan, s.jumlah, s.tanggal 
                FROM Simpanan s 
                JOIN Anggota a ON s.anggota_id = a.anggota_id
                ORDER BY s.tanggal DESC
            """)
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def show_form(mode="add", selected=None):
        form = ctk.CTkToplevel(app)
        form.title("Form Simpanan")
        form.geometry("420x400")
        form.resizable(False, False)

        # Ambil data anggota untuk dropdown
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT anggota_id, nama FROM Anggota")
            anggota_data = cursor.fetchall()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            form.destroy()
            return

        anggota_dict = {f"{nama} ({aid})": aid for aid, nama in anggota_data}

        # Komponen Form
        ctk.CTkLabel(form, text="Pilih Anggota:", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        anggota_menu = ctk.CTkOptionMenu(form, values=list(anggota_dict.keys()))
        anggota_menu.pack(padx=20, pady=5)

        ctk.CTkLabel(form, text="Jenis Simpanan:", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        jenis_menu = ctk.CTkOptionMenu(form, values=["pokok", "wajib", "sukarela"])
        jenis_menu.pack(padx=20, pady=5)

        ctk.CTkLabel(form, text="Jumlah Simpanan (Rp):", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        jumlah_entry = ctk.CTkEntry(form)
        jumlah_entry.pack(padx=20, pady=5)

        # Jika mode edit, isi dengan data lama
        if mode == "edit" and selected:
            anggota_menu.set(f"{selected[1]} ({selected[0]})")
            jenis_menu.set(selected[2])
            jumlah_entry.insert(0, str(selected[3]))

        def submit():
            try:
                anggota_id = anggota_dict.get(anggota_menu.get())
                jenis = jenis_menu.get()
                jumlah = float(jumlah_entry.get())
                tanggal = datetime.date.today().strftime("%Y-%m-%d")

                # Validasi
                if not anggota_id or not jenis or jumlah <= 0:
                    messagebox.showerror("Validasi Gagal", "Semua data harus diisi dengan benar.")
                    return

                conn = get_connection()
                cursor = conn.cursor()
                if mode == "add":
                    cursor.execute("""
                        INSERT INTO Simpanan (anggota_id, jenis_simpanan, jumlah, tanggal)
                        VALUES (?, ?, ?, ?)
                    """, (anggota_id, jenis, jumlah, tanggal))
                elif mode == "edit" and selected:
                    cursor.execute("""
                        UPDATE Simpanan
                        SET anggota_id=?, jenis_simpanan=?, jumlah=?, tanggal=?
                        WHERE simpanan_id=?
                    """, (anggota_id, jenis, jumlah, tanggal, selected[0]))
                conn.commit()
                conn.close()

                messagebox.showinfo("Sukses", "Data simpanan berhasil disimpan.")
                form.destroy()
                load_simpanan()
            except ValueError:
                messagebox.showerror("Error", "Jumlah harus berupa angka valid.")
            except Exception as e:
                messagebox.showerror("Gagal Menyimpan", str(e))

        ctk.CTkButton(form, text="💾 Simpan Data", command=submit).pack(pady=20)

    # Header & Kontrol
    ctk.CTkLabel(app.main_frame, text="📁 Kelola Data Simpanan", font=("Segoe UI", 24, "bold")).pack(pady=20)

    btn_frame = ctk.CTkFrame(app.main_frame, fg_color="transparent")
    btn_frame.pack(pady=10)

    ctk.CTkButton(btn_frame, text="➕ Tambah Simpanan", command=lambda: show_form("add")).pack(side="left", padx=10)

    def edit_selected():
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item[0], 'values')
            show_form(mode="edit", selected=values)
        else:
            messagebox.showwarning("Pilih Data", "Silakan pilih salah satu data untuk diedit.")

    ctk.CTkButton(btn_frame, text="✏️ Edit Simpanan", command=edit_selected).pack(side="left", padx=10)

    # Tabel
    table_frame = ctk.CTkFrame(app.main_frame)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ctk.CTkTabview(table_frame, columns=("ID", "Nama", "Jenis", "Jumlah", "Tanggal"), show="headings", height=15)
    tree.pack(fill="both", expand=True)

    for col in ("ID", "Nama", "Jenis", "Jumlah", "Tanggal"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    load_simpanan()
