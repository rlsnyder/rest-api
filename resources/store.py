from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            #This should return 200 as the status code, but that's the default, so it does in fact
            #return a 200 status code, we just don't have specify that explicity.
            return store.json()
        else:
            return {"Message": "Store does not exist."}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"Message": "Store already exists."}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred trying to create the store."}, 500

        return store.json(), 201


    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "Store deleted"}

class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
