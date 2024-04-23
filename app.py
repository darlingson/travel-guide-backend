from flask import Flask, jsonify, request, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
import random
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
db = SQLAlchemy(app)

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

if __name__ == "__main__":
    app.run(debug=True)
