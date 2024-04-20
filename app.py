import json
from datetime import timedelta
from flask import Flask, jsonify, request,render_template,send_file
import MySQLdb as my

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] =  ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] =  ''

def connectDB():
    db = my.connect(app.config['MYSQL_HOST'], app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_DB'])
    db.ping(True)
    return db
@app.route("/destinations")
def getDestination():
    con = connectDB()
    cur = con.cursor()
    cur.execute("SELECT * FROM places")
    rv = cur.fetchall()
    json_data = []
    row_headers = [x[0] for x in cur.description] #extracting row headers
    for result in rv:
        row_data = dict(zip(row_headers,result))
        json_data.append(row_data)
    return jsonify(json_data)
  
@app.route("/destination/image")
def getDestinationImage():
    image_name = request.args.get("path")
    full_path = "/home/Darlingson/mysite/travel-app/images/" + image_name + ".jpeg"

    return send_file(full_path, mimetype='image/gif')
