from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ensure the database file is created once
def init_db():
    if not os.path.exists('users.db'):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def payment():
    return render_template('payment.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    phone = request.form.get('phone')

    if not name or not phone:
        flash("Please fill in all details before submitting.")
        return redirect(url_for('payment'))

    # Save to database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()

    flash("Registered successfully!")
    return redirect(url_for('payment'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
