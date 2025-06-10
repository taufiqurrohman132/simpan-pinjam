import customtkinter as ctk
from tkinter import messagebox
from database import conn

def show_pinjaman(app):
    app.clear_main()

    ctk.CTkLabel(app.main_frame, text="Halaman Pinjaman", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

    frame_list = ctk.CTkFrame(app.main_frame)
    frame_list.pack(pady=10, fill="both", expand=True)

    ctk.CTkLabel(frame_list, text="Daftar Pengajuan Pinjaman", font=ctk.CTkFont(size=16)).pack(pady=10)

    listbox = ctk.CTkScrollableFrame(frame_list, height=250, width=600)
    listbox.pack(pady=5)

    def refresh_list():
        # Bersihkan isi lama
        for widget in listbox.winfo_children():
            widget.destroy()

        c = conn.cursor()
        c.execute("SELECT bunga_id, anggota_id, jumlah, tanggal_pengajuan FROM bunga WHERE status = 'diajukan'")
        pinjamans = c.fetchall()

        if not pinjamans:
            ctk.CTkLabel(listbox, text="Tidak ada pengajuan pinjaman.").pack(pady=10)
            return

        for pinjaman in pinjamans:
            bunga_id, anggota_id, jumlah, tanggal_pengajuan = pinjaman
            text = f"ID: {bunga_id} | Anggota: {anggota_id} | Jumlah: Rp{jumlah} | Tgl: {tanggal_pengajuan}"
            btn = ctk.CTkButton(listbox, text=text, command=lambda b_id=bunga_id: tampilkan_detail(b_id))
            btn.pack(pady=5, padx=10, fill="x")

    def tampilkan_detail(bunga_id):
        for widget in app.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(app.main_frame, text=f"Detail Pinjaman ID {bunga_id}", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        c = conn.cursor()
        c.execute("SELECT anggota_id, presentase, jumlah, keterangan, tenor, tgl_berlaku, status, tanggal_pengajuan FROM bunga WHERE bunga_id=?", (bunga_id,))
        data = c.fetchone()

        labels = ["Anggota ID", "Presentase", "Jumlah", "Keterangan", "Tenor", "Tanggal Berlaku", "Status", "Tanggal Pengajuan"]
        for i, value in enumerate(data):
            ctk.CTkLabel(app.main_frame, text=f"{labels[i]}: {value}", anchor="w").pack(padx=20, pady=2, fill="x")

        btn_frame = ctk.CTkFrame(app.main_frame)
        btn_frame.pack(pady=20)

        def update_status(new_status):
            c.execute("UPDATE bunga SET status=? WHERE bunga_id=?", (new_status, bunga_id))
            conn.commit()
            messagebox.showinfo("Berhasil", f"Status berhasil diperbarui ke '{new_status}'")
            show_pinjaman(app)

        ctk.CTkButton(btn_frame, text="Setujui", fg_color="green", hover_color="darkgreen", command=lambda: update_status("disetujui")).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Tolak", fg_color="red", hover_color="darkred", command=lambda: update_status("ditolak")).pack(side="right", padx=10)

    # Mulai dengan menampilkan daftar
    refresh_list()
