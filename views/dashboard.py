from tkinter import PhotoImage
import customtkinter as ctk
import sqlite3
import calendar
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_total_anggota():
    conn = sqlite3.connect("koperasi.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM anggota")
    total = c.fetchone()[0]
    conn.close()
    return total

def get_simpanan_per_bulan():
    conn = sqlite3.connect("koperasi.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT strftime('%Y-%m', tanggal), SUM(jumlah)
        FROM simpanan
        GROUP BY strftime('%Y-%m', tanggal)
        ORDER BY strftime('%Y-%m', tanggal) ASC
    """)
    data = cursor.fetchall()
    conn.close()
    return zip(*data) if data else ([], [])

def get_simpanan_filtered(bulan_nama, tahun):
    bulan_num = list(calendar.month_name).index(bulan_nama)
    bulan_str = f"{bulan_num:02}"
    date_prefix = f"{tahun}-{bulan_str}"

    conn = sqlite3.connect("koperasi.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT strftime('%Y-%m-%d', tanggal), SUM(jumlah)
        FROM simpanan
        WHERE strftime('%Y-%m', tanggal) = ?
        GROUP BY strftime('%Y-%m-%d', tanggal)
        ORDER BY tanggal ASC
    """, (date_prefix,))
    data = cursor.fetchall()
    conn.close()
    return zip(*data) if data else ([], [])

def get_pinjaman_per_bulan():
    conn = sqlite3.connect("koperasi.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT strftime('%Y-%m', tanggal_pengajuan), SUM(jumlah)
        FROM pinjaman
        GROUP BY strftime('%Y-%m', tanggal_pengajuan)
        ORDER BY strftime('%Y-%m', tanggal_pengajuan) ASC
    """)
    data = cursor.fetchall()
    conn.close()
    return zip(*data) if data else ([], [])

def get_pinjaman_filtered(bulan_nama, tahun):
    bulan_num = list(calendar.month_name).index(bulan_nama)
    bulan_str = f"{bulan_num:02}"
    date_prefix = f"{tahun}-{bulan_str}"

    conn = sqlite3.connect("koperasi.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT strftime('%Y-%m-%d', tanggal_pengajuan), SUM(jumlah)
        FROM pinjaman
        WHERE strftime('%Y-%m', tanggal_pengajuan) = ?
        GROUP BY strftime('%Y-%m-%d', tanggal_pengajuan)
        ORDER BY tanggal_pengajuan ASC
    """, (date_prefix,))
    data = cursor.fetchall()
    conn.close()
    return zip(*data) if data else ([], [])

def show_dashboard(app):
    app.clear_main()

    ctk.CTkLabel(app.main_frame, text=f"👋 Selamat Datang, {app.user[1]}",
                 font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(30, 10))

    stats_frame = ctk.CTkFrame(app.main_frame, fg_color="transparent")
    stats_frame.pack(padx=30, pady=10, fill="x")

    def stat_card(parent, title, value, emoji, color):
        card = ctk.CTkFrame(parent, width=200, height=120, corner_radius=15, fg_color=color)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=emoji, font=ctk.CTkFont(size=32)).pack(pady=(10, 0))
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack()
        ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=22)).pack()
        return card

    total_anggota = get_total_anggota()
    stat_card(stats_frame, "Total Anggota", total_anggota, "👥", "#3b8b56").pack(side="left", padx=10)

    if app.user and len(app.user) > 3 and app.user[3] == "admin":
        filter_frame = ctk.CTkFrame(app.main_frame, fg_color="transparent")
        filter_frame.pack(padx=30, pady=(20, 5), fill="x")

        bulan_options = list(calendar.month_name)[1:]
        tahun_options = [str(t) for t in range(2020, datetime.now().year + 1)]

        bulan_var = ctk.StringVar(value=datetime.now().strftime('%B'))
        tahun_var = ctk.StringVar(value=str(datetime.now().year))

        ctk.CTkLabel(filter_frame, text="Bulan:").pack(side="left", padx=(0, 5))
        ctk.CTkComboBox(filter_frame, values=bulan_options, variable=bulan_var).pack(side="left")

        ctk.CTkLabel(filter_frame, text="Tahun:").pack(side="left", padx=(10, 5))
        ctk.CTkComboBox(filter_frame, values=tahun_options, variable=tahun_var).pack(side="left")

        chart_frame = ctk.CTkFrame(app.main_frame)
        chart_frame.pack(padx=30, pady=10, fill="both", expand=True)

        def tampilkan_grafik(bulan=None, tahun=None):
            for widget in chart_frame.winfo_children():
                widget.destroy()

            if bulan and tahun:
                simp_labels, simp_values = get_simpanan_filtered(bulan, tahun)
                pinj_labels, pinj_values = get_pinjaman_filtered(bulan, tahun)
                simp_title = f"Simpanan Bulan {bulan} {tahun}"
                pinj_title = f"Pinjaman Bulan {bulan} {tahun}"
            else:
                simp_labels, simp_values = get_simpanan_per_bulan()
                pinj_labels, pinj_values = get_pinjaman_per_bulan()
                simp_title = "Tren Simpanan per Bulan"
                pinj_title = "Tren Pinjaman per Bulan"

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))

            ax1.bar(simp_labels, simp_values, color="#3b8b56")
            ax1.set_title(simp_title)
            ax1.set_ylabel("Jumlah")
            ax1.set_xticks(range(len(simp_labels)))
            ax1.set_xticklabels(simp_labels, rotation=45, ha='right')

            ax2.bar(pinj_labels, pinj_values, color="#c2513f")
            ax2.set_title(pinj_title)
            ax2.set_ylabel("Jumlah")
            ax2.set_xticks(range(len(pinj_labels)))
            ax2.set_xticklabels(pinj_labels, rotation=45, ha='right')

            fig.tight_layout()
            chart = FigureCanvasTkAgg(fig, chart_frame)
            chart.get_tk_widget().pack(fill="both", expand=True)

        def apply_filter():
            tampilkan_grafik(bulan_var.get(), tahun_var.get())

        ctk.CTkButton(filter_frame, text="Terapkan Filter", command=apply_filter).pack(side="left", padx=(10, 0))

        tampilkan_grafik()
