from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
	#Configure a parser to use with the JSON data to require price and store-id data be passed in the JSON data
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float,
		required=True,
		help="This field may not be left blank."
	)
	parser.add_argument('store_id',
		type=int,
		required=True,
		help="Every item must have a store_id"
	)

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()

		return {"message": "Item does not exist"}, 404

	@jwt_required()
	def post(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return {"message": f"An item with the name '{name}' already exists."}, 400

		data = Item.parser.parse_args()

		#"**data" = argument unpacking, makes the code more succinct
		item = ItemModel(name, **data)

		try:
			item.save_to_db()
		except:
			# 500 is the response code for "internal server error"
			# This is the most logical thing to return because an item failing to insert is not the user's fault - an error on our API's side occured.
			return {"message": "An error occurred trying to insert the item."}, 500

		return item.json(), 201

	@jwt_required()
	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {"message": "Item deleted"}

	@jwt_required()
	def put(self, name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)

		if item is None:
			#Creates an item if one doesn't exist
			item = ItemModel(name, **data)
		else:
			# Updates price of existing item (defined outside of this conditional if/else block)
			# if the item already exists in the db.
			item.price = data['price']

		# either way, if new "item" had to be created in if/else block, or if we updated an exisiting item, This
		# save_to_db method takes care of modifying the database accordingly.
		item.save_to_db()

		return item.json()


class ItemList(Resource):
	@jwt_required()
	def get(self):
		return {"items": [item.json() for item in ItemModel.query.all()]}
