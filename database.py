import sqlite3

conn = sqlite3.connect("koperasi.db", check_same_thread=False)
c = conn.cursor()
