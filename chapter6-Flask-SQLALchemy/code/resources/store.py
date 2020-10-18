from flask_restful import Resource, reqparse

from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        item = StoreModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "Sorry, store existed"}, 400

        new_item = StoreModel(name)
        try:
            new_item.save_to_db()
        except:
            return {"message": "An error occurred when inserting"}, 500

        return new_item.json(), 201

    def delete(self, name):
        item = StoreModel.find_by_name(name)
        if item: item.delete_from_db()
        return {"message": "Store deleted"}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
