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
@app.route("/destinations/spotlight")
def getSpotlight():
    try:
        con = connectDB()
        cur = con.cursor()
        cur.execute("SELECT * FROM places")
        all_entries = cur.fetchall()
        if all_entries:
            random_entry = random.choice(all_entries)
            # Assuming the columns in the 'places' table are 'id', 'name', 'description', 'district', 'location', 'link', 'latitude', 'longitude', 'image_paths', and 'image_copyrite_holders'
            entry_dict = {
                'id': random_entry[0],
                'name': random_entry[1],
                'description': random_entry[2],
                'district': random_entry[3],
                'location': random_entry[4],
                'link': random_entry[5],
                'latitude': random_entry[6],
                'longitude': random_entry[7],
                'image_paths': random_entry[8],
                'image_copyrite_holders': random_entry[9]
            }
            return jsonify(entry_dict)
        else:
            return jsonify({'message': 'No entries found in the database'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/destinations/<id>")
def getDestinationById(id):
    cur = db.cursor ()
    cur.execute("SELECT * FROM places WHERE id = %s", (id,))
    rv = cur.fetchall()
    json_data = []
    row_headers = [x[0] for x in cur.description] #extracting row headers
    for result in rv:
        row_data = dict(zip(row_headers,result))
        json_data.append(row_data)
    return jsonify(json_data)@app.route('/login', methods=['POST'])

def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Please provide both username and password'}), 400

        db = connectDB()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            db.close()
            return jsonify({'message': 'Logged in successfully!'}), 200
        else:
            db.close()
            return jsonify({'message': 'Incorrect username or password'}), 401

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return jsonify({'message': 'Please provide username, password, and email'}), 400

        db = connectDB()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            db.close()
            return jsonify({'message': 'Account already exists'}), 409

        cursor.execute('INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)',
                       (username, password, email))
        db.close()
        return jsonify({'message': 'You have successfully registered'}), 201
