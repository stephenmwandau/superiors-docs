#!/usr/bin/env python3

from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from models import db
from routes import configure_routes

# instantiate Flask app
app = Flask(__name__)

# configure Flask app with SQLAlchemy settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# manage cross-origin issues
CORS(app)

# initialize Flask-Migrate app and SQLAlchemy instance
migrate = Migrate(app, db)

# initialize the db with app
db.init_app(app)

# configure the routes
configure_routes(app)

# executed only if run/not if imported
if __name__ == '__main__':
    app.run(port=5555, debug=True)
