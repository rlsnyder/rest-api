import sqlite3
from db import db

class UserModel(db.Model):

	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	password = db.Column(db.String(80))

	def __init__(self, username, password):
		self.username = username
		self.password = password

	@classmethod
	def find_by_username(cls, username):
		#since we indicated at the top that __tablename__ = 'users', cls.query, the query builder,
		#returns "SELECT * FROM users" - however, we must filter this result to only include
		#some users, which is what the filter_by method is for.
		return cls.query.filter_by(username=username).first()

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
