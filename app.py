from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
#Tells SQLAlchemy where the database file is so SQLAlchemy can work :)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#This config turns off flask's SQLAlchemy from tracking changes, and let's SQLAlchemy itself track the changes.
#I made a note in video 97 of the Udemy API Course though, at 8:24 when Jose explains it. See that if needed!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'logan'
api = Api(app)

@app.before_first_request
def create_tables():
	db.create_all()

jwt = JWT(app, authenticate, identity) #endpoint: /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items/')
api.add_resource(StoreList, '/stores/')

api.add_resource(UserRegister, '/register')

# This makes it so the app only runs if it is called to run from this file. Otherwise it doesn't run if we imported it from elsewhere?
# Don't reall understand it. See video 84 in Section 5 of Udemy course on REST APIs with Flask and Python.
if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True, use_reloader=False)
