from flask import Flask, jsonify, request, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
import random
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import URLSafeTimedSerializer as Serializer
# from flask import Flask
from flask_bootstrap import Bootstrap
# from flask import jsonify
# import json
# from datetime import timedelta
# from flask import Flask, jsonify, request,render_template,send_file
# import MySQLdb as my
# import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@host/databasename'
app.config['SECRET_KEY'] = 'secret_key'
app.config['TOKEN_EXPIRATION_SECONDS'] = 3600 
db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

class Zochitika(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    address = db.Column(db.String(255))

    def serialize(self):
        return {
            'id': self.id,
            'date': str(self.date),
            'time': str(self.time),
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'address': self.address
        }

class Places(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    district = db.Column(db.String(255))
    location = db.Column(db.String(255))
    link = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    image_paths = db.Column(db.String(255))
    image_copyrite_holders = db.Column(db.String(255))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'district': self.district,
            'location': self.location,
            'link': self.link,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_paths': self.image_paths,
            'image_copyrite_holders': self.image_copyrite_holders
        }

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/zochitika')
def getZochitikaAll():
    zochitika_entries = Zochitika.query.order_by(Zochitika.date.desc(), Zochitika.time.desc()).all()
    return jsonify([entry.serialize() for entry in zochitika_entries])

@app.route('/zochitika/<int:id>')
def getZochitikaById(id):
    zochitika_entry = Zochitika.query.get(id)
    return jsonify(zochitika_entry.serialize())

@app.route('/destinations')
def getDestinations():
    destinations = Places.query.all()
    return jsonify([destination.serialize() for destination in destinations])

@app.route('/destinations/<int:id>')
def getDestinationById(id):
    destination = Places.query.get(id)
    return jsonify(destination.serialize())

@app.route("/zochitika/poster")
def getPoster():
    poster_name = request.args.get("path")
    full_path = "/home/Darlingson/mysite/zochitika/posters/" + poster_name + ".jpeg"
    return send_file(full_path, mimetype='image/jpeg')

@app.route("/destination/image")
def getDestinationImage():
    image_name = request.args.get("path")
    full_path = "/home/Darlingson/mysite/travel-app/images/" + image_name + ".jpg"
    return send_file(full_path, mimetype='image/jpeg')

@app.route("/destinations/recommendations")
def getRecommendations():
    destinations = Places.query.all()
    random.shuffle(destinations)
    return jsonify([destination.serialize() for destination in destinations])

@app.route("/destinations/spotlight")
def getSpotlight():
    try:
        all_entries = Places.query.all()
        if all_entries:
            random_entry = random.choice(all_entries)
            return jsonify(random_entry.serialize())
        else:
            return jsonify({'message': 'No entries found in the database'})
    except Exception as e:
        return jsonify({'error': str(e)})
@app.route('/destinations/search', methods=['GET'])
def search_destination():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword parameter is required'}), 400

    results = Places.query.filter(Places.name.ilike(f'%{keyword}%')).all()

    if results:
        destinations = [
            {'id': dest.id, 'name': dest.name, 'location': dest.location,'district':dest.district,'image_paths':dest.image_paths} for dest in results]
        return jsonify({'results': destinations}), 200
    else:
        return jsonify({'message': 'No destinations found for the given keyword'}), 404

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

# Generate Token
def generate_token(user_id):
    s = Serializer(app.config['SECRET_KEY'], expires_in=app.config['TOKEN_EXPIRATION_SECONDS'])
    return s.dumps({'user_id': user_id}).decode('utf-8')

# Routes for login, register, and logout
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        login_user(user)
        token = generate_token(user.id)
        return jsonify({'message': 'Login successful', 'token': token}), 200
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

# Protected route example
@app.route('/protected')
@login_required
def protected():
    return jsonify({'message': f'Hello, {current_user.username}! This is a protected route'}), 200

if __name__ == "__main__":
    app.run(debug=True)
