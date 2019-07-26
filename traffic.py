from flask import Flask, render_template, request, flash
import sqlite3 as lite
from datetime import datetime
from config import credential
import os

app = Flask(__name__)
app.config['SECRET_KEY']='8ac7f84d2b39bffc88d30b3616069d'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def select_records():
    rows = []
    try:
        with lite.connect('traffic.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute('SELECT * FROM data')
            rows = cur.fetchall()
    except lite.Error as error:
        con.rollback()
        print(error.args[0])
        return False
    finally:
        con.close()
        return rows


@app.route('/')
def login():
    return render_template('login.html')


@app.route("/login", methods = ['GET', 'POST'])
@app.route("/index", methods=["GET", "POST"])
def index():
    print("landing page running...")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # credentials from config files imported
        if username == credential['username'] and password == credential['password']:
            flash('Login successful :)', 'success')
            # flash("You have successfully logged in.", 'success')    # python Toastr uses flash to flash pages
            return render_template('index.html')
        else:
            flash('Login Unsuccessful. Please check username and password', 'error')

    data = select_records()
    return render_template('index.html', data = data)


@app.route('/addrec', methods=['POST'])
def add_record():
    try:
        image_url = request.form['image_url']
        timestamp = request.form['timestamp']
        speed = request.form['speed']
        camera = request.form['camera']

        with lite.connect('traffic.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO data(image, time_stamp, speed, camera_id) VALUES(?, ?, ?, ?)', (image_url, timestamp, speed, camera))

            con.commit()
            msg = (datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ' Record successfully added!'
    except:
        con.rollback()
        msg = 'error occured'
    finally:
        con.close()
        return msg


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)