import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="This field may not be left blank."
	)
	parser.add_argument('password',
		type=str,
		required=True,
		help="This field may not be left blank."
	)
	
	#The password is passed as JSON plain text - obviously you wouldn't do this in a real REST API, this was more of a learning exercise.

	def post(self):
		data = UserRegister.parser.parse_args()

		if UserModel.find_by_username(data['username']):
			return {"message": "User already exists."}, 400

		#**data used for argument unpacking - the parser creates a dictionary with username and password, so we
		#can unpack those while constructing the UserModel.
		user = UserModel(**data)
		user.save_to_db()

		return {"message": "User created successfully"}, 201
