import customtkinter as ctk
from tkinter import messagebox
import datetime
from database import conn  # ambil koneksi global
from helper import helper

def show_simpanan(app):
    app.clear_main()

    def load_simpanan():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        try:
            cursor = conn.cursor()
            print("[DEBUG] Koneksi load_simpanan dibuka")
            cursor.execute("""
                SELECT s.id_simpanan, a.nama, s.jenis_simpanan, s.jumlah, s.tanggal 
                FROM Simpanan s 
                JOIN Anggota a ON s.id_anggota = a.id_anggota
                ORDER BY s.tanggal DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            print(f"[DEBUG] Jumlah data yang diambil: {len(rows)}")
            print("[DEBUG] Koneksi load_simpanan ditutup")

            for i, row in enumerate(rows):
                row_frame = ctk.CTkFrame(scrollable_frame, fg_color="black")
                row_frame.pack(fill="x", padx=10, pady=5)

                row_frame.grid_columnconfigure(0, weight=0)  # ID tetap
                for col in range(1, 5):
                    row_frame.grid_columnconfigure(col, weight=1)  # Kolom 1–4 melar

                # Label untuk ID
                ctk.CTkLabel(row_frame, text=str(row[0]), anchor="w").grid(
                    row=0, column=0, padx=5, pady=5, sticky="ew"
                )

                # Entry untuk kolom 1–4
                for col in range(1, 5):
                    val = row[col]
                    # Format uang untuk kolom ke-3 (index ke-3 = column=3)
                    if col == 3 and isinstance(val, (int, float)):
                        val = f"{val:,.0f}"
                    entry = ctk.CTkEntry(row_frame, border_width=0, fg_color="transparent")
                    entry.insert(0, str(val))
                    entry.grid(row=0, column=col, padx=2, pady=5, sticky="ew")

                # Tombol aksi
                ctk.CTkButton(
                    row_frame, text="✏️", command=lambda r=row: show_form("edit", r), width=80
                ).grid(row=0, column=5, padx=5, pady=5)

                ctk.CTkButton(
                    row_frame, text="🗑️", fg_color="red", hover_color="#cc3333", width=80,
                    command=lambda r=row: delete_simpanan(r[0])
                ).grid(row=0, column=6, padx=5, pady=5)

        except Exception as e:
            print(f"[ERROR] load_simpanan: {e}")
            messagebox.showerror("Database Error", str(e))

    def delete_simpanan(id_simpanan):
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            try:
                cursor = conn.cursor()
                print(f"[DEBUG] Koneksi delete_simpanan dibuka untuk id_simpanan={id_simpanan}")
                cursor.execute("DELETE FROM Simpanan WHERE id_simpanan = ?", (id_simpanan,))
                conn.commit()
                cursor.close()
                print("[DEBUG] Delete berhasil dan koneksi ditutup")
                load_simpanan()
            except Exception as e:
                print(f"[ERROR] delete_simpanan: {e}")
                messagebox.showerror("Gagal Menghapus", str(e))


    form = None
    def show_form(mode="add", selected=None):
        nonlocal form
        if form is not None and form.winfo_exists():
            form.focus()
            return
        
        form = ctk.CTkToplevel(app)
        form.title("Form Simpanan")
        form.geometry("420x400")
        form.resizable(False, False)
        form.grab_set()
        helper.center_window(form, 420, 400)

        try:
            cursor = conn.cursor()
            print("[DEBUG] Koneksi show_form (ambil anggota) dibuka")
            cursor.execute("SELECT id_anggota, nama FROM Anggota")
            anggota_data = cursor.fetchall()
            cursor.close()
            print(f"[DEBUG] Jumlah anggota yang diambil: {len(anggota_data)}")
            print("[DEBUG] Koneksi show_form ditutup")
        except Exception as e:
            print(f"[ERROR] show_form ambil anggota: {e}")
            messagebox.showerror("Database Error", str(e))
            form.destroy()
            return

        anggota_dict = {f"{nama} ({aid})": aid for aid, nama in anggota_data}
        anggota_keys = list(anggota_dict.keys())

        ctk.CTkLabel(form, text="Pilih Anggota:", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        anggota_menu = ctk.CTkOptionMenu(form, values=anggota_keys)
        anggota_menu.pack(padx=20, pady=5)

        ctk.CTkLabel(form, text="Jenis Simpanan:", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        jenis_menu = ctk.CTkOptionMenu(form, values=["pokok", "wajib", "sukarela"])
        jenis_menu.pack(padx=20, pady=5)

        ctk.CTkLabel(form, text="Jumlah Simpanan (Rp):", anchor="w").pack(fill="x", padx=20, pady=(10, 2))
        jumlah_entry = ctk.CTkEntry(form)
        jumlah_entry.pack(padx=20, pady=5)

        if mode == "edit" and selected:
            anggota_menu.set(f"{selected[1]} ({selected[0]})")
            jenis_menu.set(selected[2])
            jumlah_entry.insert(0, str(selected[3]))

        def submit():
            try:
                anggota_nama = anggota_menu.get()
                anggota_id = anggota_dict.get(anggota_nama)
                jenis = jenis_menu.get()
                jumlah_str = jumlah_entry.get().replace(",", "").strip()
                tanggal = datetime.date.today().strftime("%Y-%m-%d")

                if not anggota_id or not jenis or not jumlah_str:
                    messagebox.showerror("Validasi Gagal", "Semua data harus diisi.")
                    return

                jumlah = float(jumlah_str)
                if jumlah <= 0:
                    raise ValueError("Jumlah harus lebih dari 0")

                cursor = conn.cursor()
                print("[DEBUG] Koneksi submit dibuka")
                if mode == "add":
                    print("menambahkan")
                    cursor.execute("""
                        INSERT INTO Simpanan (id_anggota, jenis_simpanan, jumlah, tanggal)
                        VALUES (?, ?, ?, ?)
                    """, (anggota_id, jenis, jumlah, tanggal))
                elif mode == "edit" and selected:
                    id_simpanan = selected[0]
                    print("mengupdate")
                    cursor.execute("""
                        UPDATE Simpanan
                        SET id_anggota=?, jenis_simpanan=?, jumlah=?, tanggal=?
                        WHERE id_simpanan=?
                    """, (anggota_id, jenis, jumlah, tanggal, id_simpanan))
                conn.commit()
                cursor.close()
                print("[DEBUG] Data simpanan disimpan dan koneksi submit ditutup")

                messagebox.showinfo("Sukses", "Data simpanan berhasil disimpan.")
                form.destroy()
                load_simpanan()
            except ValueError:
                messagebox.showerror("Error", "Jumlah harus berupa angka yang valid dan lebih dari 0.")
            except Exception as e:
                print(f"[ERROR] submit: {e}")
                messagebox.showerror("Gagal Menyimpan", str(e))

        ctk.CTkButton(form, text="💾 Simpan Data", command=submit).pack(pady=20)

    # Tampilan utama
    ctk.CTkLabel(app.main_frame, text="📁 Data Simpanan", font=("Segoe UI", 24, "bold"), anchor="w").pack(fill="x", padx=20, pady=(10, 5))
    ctk.CTkButton(app.main_frame, text="➕ Tambah Simpanan", command=lambda: show_form("add"), width=200).pack(padx=20, anchor="w")

    search_frame = ctk.CTkFrame(app.main_frame, fg_color="transparent")
    search_frame.pack(fill="x", padx=20, pady=(5, 10))
    ctk.CTkEntry(search_frame, placeholder_text="🔍 Cari nama anggota", width=300).pack(side="left")

    scroll_frame = ctk.CTkFrame(app.main_frame)
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

    scrollable_frame = ctk.CTkScrollableFrame(scroll_frame)
    scrollable_frame.pack(fill="both", expand=True)

    header = ctk.CTkFrame(scrollable_frame, fg_color="#f0f0f0")
    header.pack(fill="x", padx=10, pady=5)
    for i, title in enumerate(["ID", "Nama", "Jenis", "Jumlah", "Tanggal", "Edit", "Hapus"]):
        ctk.CTkLabel(header, text=title, font=("Segoe UI", 12, "bold"), anchor="w").grid(row=0, column=i, padx=5, pady=5)

    load_simpanan()
