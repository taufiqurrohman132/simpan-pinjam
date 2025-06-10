from database import conn
import customtkinter as ctk

def show_pinjaman(app):
    app.clear_main()

    # ========= HEADER TITLE =========
    header = ctk.CTkFrame(app.main_frame, fg_color="transparent")
    header.pack(fill="x", padx=20, pady=(20, 0))

    ctk.CTkLabel(
        header, text="📄 Halaman Pinjaman",
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color="#00ADB5"
    ).pack(anchor="w")

    ctk.CTkLabel(
        header, text="Kelola pengajuan pinjaman anggota dengan tampilan modern.",
        font=ctk.CTkFont(size=13), text_color="#888888"
    ).pack(anchor="w", pady=(0, 10))

    # ========= STATISTIK =========
    stats_frame = ctk.CTkFrame(app.main_frame, fg_color="#FFFFFF")
    stats_frame.pack(fill="x", padx=20, pady=10)

    def stat_card(text, value, color):
        frame = ctk.CTkFrame(stats_frame, corner_radius=10, fg_color=color, width=200, height=70)
        frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=14), text_color="#FFFFFF").pack()
        ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=18, weight="bold"), text_color="#FFFFFF").pack()

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), AVG(tenor), SUM(jumlah) FROM pinjaman WHERE status='diajukan'")
    count, avg_tenor, total = cursor.fetchone()

    stat_card("Jumlah Pinjaman", f"{count or 0} data", "#00ADB5")
    stat_card("Total Diajukan", f"Rp {total or 0:,.0f}", "#393E46")
    stat_card("Rata-rata Tenor", f"{round(avg_tenor or 0):.0f} bulan", "#FF5722")

    # ========= FILTER & SEARCH =========
    filter_frame = ctk.CTkFrame(app.main_frame, fg_color="transparent")
    filter_frame.pack(fill="x", padx=20)

    search_var = ctk.StringVar()
    ctk.CTkEntry(filter_frame, placeholder_text="🔍 Cari keterangan...", textvariable=search_var, width=250).pack(side="left", padx=(0, 10))

    status_filter = ctk.CTkOptionMenu(
        filter_frame,
        values=["Semua", "Diajukan", "Disetujui", "Lunas"],
        width=140
    )
    status_filter.set("Diajukan")
    status_filter.pack(side="left")

    ctk.CTkButton(filter_frame, text="🔄 Refresh", command=lambda: show_pinjaman(app)).pack(side="right")

    # ========= SCROLLABLE LIST =========
    list_frame = ctk.CTkScrollableFrame(app.main_frame, fg_color="#F4F4F4", height=450)
    list_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

    # Ambil data pinjaman
    cursor.execute("""
        SELECT p.bunga_id, p.jumlah, b.presentase, p.tenor, p.keterangan,
               p.tgl_berlaku, p.tanggal_pengajuan, p.status
        FROM pinjaman p
        JOIN bunga b ON p.id_bunga = b.id_bunga
        WHERE p.status = 'diajukan'
    """)
    rows = cursor.fetchall()

    def status_color(s):
        return {"diajukan": "#FF9800", "disetujui": "#4CAF50", "lunas": "#F44336"}.get(s.lower(), "#9E9E9E")

    if not rows:
        ctk.CTkLabel(
            list_frame, text="📭 Tidak ada data pinjaman saat ini.",
            font=ctk.CTkFont(size=16, weight="bold"), text_color="#777"
        ).pack(pady=30)
        return

    # Tampilkan tiap pinjaman
    for bunga_id, jumlah, bunga, tenor, ket, tgl_berlaku, tgl_pengajuan, status in rows:
        card = ctk.CTkFrame(list_frame, corner_radius=12, fg_color="#FFFFFF", border_color="#E0E0E0", border_width=1)
        card.pack(fill="x", pady=10, padx=10)

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=15, pady=(10, 0))

        ctk.CTkLabel(top, text=f"ID Bunga #{bunga_id}", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")

        ctk.CTkLabel(
            top, text=status.upper(),
            font=ctk.CTkFont(size=12),
            text_color="#FFFFFF",
            fg_color=status_color(status),
            corner_radius=8, padx=10, pady=4
        ).pack(side="right")

        # Info rows
        info_data = [
            ("Jumlah", f"Rp {jumlah:,.0f}"),
            ("Bunga", f"{bunga}%"),
            ("Tenor", f"{tenor} bulan"),
            ("Tgl Berlaku", tgl_berlaku),
            ("Tgl Pengajuan", tgl_pengajuan),
            ("Keterangan", ket)
        ]

        for label, value in info_data:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=2)
            ctk.CTkLabel(row, text=label, width=130, anchor="w", text_color="#666").pack(side="left")
            ctk.CTkLabel(row, text=value, anchor="w", text_color="#111").pack(side="left")

        # Aksi tombol
        action_row = ctk.CTkFrame(card, fg_color="transparent")
        action_row.pack(padx=15, pady=10)

        ctk.CTkButton(action_row, text="📋 Detail", fg_color="#00BCD4", hover_color="#0097A7", corner_radius=6).pack(side="left", padx=5)
        ctk.CTkButton(action_row, text="🗑️ Hapus", fg_color="#FF5252", hover_color="#E53935", corner_radius=6).pack(side="left", padx=5)
