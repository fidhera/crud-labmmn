import sqlite3

conn = sqlite3.connect('database/data.db')
conn.execute('''
    CREATE TABLE praktikan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        npm TEXT,
        nama TEXT,
        kelas TEXT,
        kehadiran INTEGER,
        lp INTEGER,
        la INTEGER,
        ujian INTEGER
    )
''')
conn.commit()
conn.close()

print("database berhasil dibuat.")
