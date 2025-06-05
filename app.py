from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'rahasia'

def get_db():
    conn = sqlite3.connect('database/data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['user'] = 'admin'
            return redirect('/praktikan')
        else:
            return redirect(url_for('login', error=1))
    return render_template('login.html')

@app.route('/praktikan')
def praktikan():
    if 'user' not in session:
        return redirect('/')
    conn = get_db()
    rows = conn.execute('SELECT * FROM praktikan').fetchall()
    return render_template('data_praktikan.html', data=rows)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        conn = get_db()
        conn.execute('INSERT INTO praktikan (npm, nama, kelas, kehadiran, lp, la, ujian) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (request.form['npm'], request.form['nama'], request.form['kelas'],
                      request.form['kehadiran'], request.form['lp'], request.form['la'], request.form['ujian']))
        conn.commit()
        return redirect('/praktikan')
    return render_template('form_praktikan.html', action="Tambah", data={})

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    if request.method == 'POST':
        conn.execute('UPDATE praktikan SET npm=?, nama=?, kelas=?, kehadiran=?, lp=?, la=?, ujian=? WHERE id=?',
                     (request.form['npm'], request.form['nama'], request.form['kelas'],
                      request.form['kehadiran'], request.form['lp'], request.form['la'], request.form['ujian'], id))
        conn.commit()
        return redirect('/praktikan')
    data = conn.execute('SELECT * FROM praktikan WHERE id=?', (id,)).fetchone()
    return render_template('form_praktikan.html', action="Edit", data=data)

@app.route('/hapus/<int:id>')
def hapus(id):
    conn = get_db()
    conn.execute('DELETE FROM praktikan WHERE id=?', (id,))
    conn.commit()
    return redirect('/praktikan')

if __name__ == '__main__':
    app.run(debug=True, port=5050)

