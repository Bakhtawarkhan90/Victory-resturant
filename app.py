from flask import Flask, request, redirect, url_for, send_from_directory
import mysql.connector
import os
import time

app = Flask(__name__, static_url_path='/static', static_folder='.')

# Connect to MySQL with retry
while True:
    try:
        db = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "database"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "kali"),
            database=os.getenv("MYSQL_DATABASE", "reservation")
        )
        print("Database connected")
        break
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        time.sleep(5)

# Create reservations table
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    day VARCHAR(20),
    hour VARCHAR(10),
    name VARCHAR(100),
    phone VARCHAR(20),
    person INT
)
""")
cursor.close()

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/reserve', methods=['POST'])
def reserve():
    day = request.form['day']
    hour = request.form['hour']
    name = request.form['name']
    phone = request.form['phone']
    person = request.form['person']

    try:
        cursor = db.cursor()
        query = "INSERT INTO reservations (day, hour, name, phone, person) VALUES (%s, %s, %s, %s, %s)"
        values = (day, hour, name, phone, int(person))
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        print("Reservation saved.")
    except mysql.connector.Error as err:
        print(f"Insert error: {err}")

    return redirect(url_for('thank_you'))

@app.route('/thankyou')
def thank_you():
    return send_from_directory(os.getcwd(), 'thankyou.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
