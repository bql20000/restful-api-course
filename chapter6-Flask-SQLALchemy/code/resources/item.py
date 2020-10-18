from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,  # automatically typecast data
                        required=True
                        )
    parser.add_argument('store_id',
                        type=int,  # automatically typecast data
                        required=True
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "Sorry, Item existed"}, 400
        data = Item.parser.parse_args()
        new_item = ItemModel(name, **data)
        try:
            new_item.save_to_db()
        except:
            return {"message": "An error occurred when inserting"}, 500

        return new_item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()
        return item.json(), 200

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item: item.delete_from_db()
        return {"message": "Item deleted"}


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
