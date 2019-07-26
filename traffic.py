from flask import Flask, render_template, request
import sqlite3 as lite
from datetime import datetime
import os

app = Flask(__name__)

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
def index():
    data = select_records()
    return render_template('home.html', data = data)


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