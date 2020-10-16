import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,  # automatically typecast data
                        required=True
                        )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message": "Item not found"}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        name_query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(name_query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[1], "price": row[2]}}

    def post(self, name):
        if Item.find_by_name(name):
            return {"message": "Sorry, Item existed"}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            Item.insert(item)
        except:
            return {"message": "An error occurred when inserting"}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO items VALUES (NULL, ?, ?)"
        cursor.execute(insert_query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        update_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(update_query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    def put(self, name):
        data = Item.parser.parse_args()

        updated_item = {'name': name, 'price': data['price']}

        if Item.find_by_name(name):
            try:
               Item.update(updated_item)
            except:
                return {"message": "An error occurred when updating"}, 500
        else:
            #cursor.execute(insert_query, (name, data['price']))
            try:
                Item.insert(updated_item)
            except:
                return {"message": "An error occurred when inserting"}, 500

        return updated_item, 200


    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        del_query = "DELETE FROM items WHERE name=?"
        cursor.execute(del_query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        del_query = "SELECT * from items"
        result = cursor.execute(del_query)
        items = []
        for row in result:
            items.append({'name': row[1], 'price': row[2]})
        connection.commit()
        connection.close()
        return {'items': items}
