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
@app.route("/destinations/recommendations")
def getRecommendations():
    con = connectDB()
    cur = con.cursor()
    cur.execute("SELECT * FROM places")
    rv = cur.fetchall()
    json_data = []
    row_headers = [x[0] for x in cur.description] #extracting row headers
    for result in rv:
        row_data = dict(zip(row_headers,result))
        json_data.append(row_data)
    random.Random(random_seed(6)).shuffle(json_data)
    return jsonify(json_data)

def random_seed(length):
    random.seed()  # Initialize the random number generator
    min_value = 10**(length - 1)
    max_value = 9 * min_value + (min_value - 1)
    return random.randint(min_value, max_value)
