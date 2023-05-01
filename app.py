from flask import Flask, render_template, request
import os
from passlib.hash import pbkdf2_sha256
import psycopg2
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__,static_folder='static')
conn = psycopg2.connect(
        host=os.environ.get("HOST_DB"),
        user=os.environ.get("USER_DB"),
        password=os.environ.get("PASSWORD_DB"),
        database=os.environ.get("NAME_DB"),
        port=os.environ.get("PORT_DB")
    )
conn.autocommit = True

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['name']
        password = request.form['password']
        hashed_password = pbkdf2_sha256.hash(password)
        print(len(hashed_password))
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, password) VALUES (%s, %s)", (name, hashed_password))
        conn.commit()
        return render_template('mail.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['name']
        password = request.form['password']
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE name = %s", (name,))
        row = cursor.fetchone()
        if row is None:
            return "User not found"
        hashed_password = row[0]
        print(row)
        print(hashed_password)
        print(len(hashed_password))
        if pbkdf2_sha256.verify(password, hashed_password):
            return main_mail()
        else:
            return "Invalid credentials"

@app.route('/account/', methods=['GET','POST'])
def account_view():
    return render_template('account.html')

@app.route('/', methods=['GET','POST'])
def main_mail():
    return render_template('mail.html')

@app.route('/letter/', methods=['GET'])
def letter_view():
    return render_template('letter.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)