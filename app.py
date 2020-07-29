#Gives us access to environment variables
import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
#Tells SQLAlchemy where the database file is so SQLAlchemy can work 
#Here it gets the database url/uri from a Heroku environment variable.
#second argument of "sqlite:/// ..." is to still be able to run this app locally if Heroku app is not up.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'logan'
api = Api(app)

jwt = JWT(app, authenticate, identity) #endpoint: /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items/')
api.add_resource(StoreList, '/stores/')

api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True, use_reloader=False)
