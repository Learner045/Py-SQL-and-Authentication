import sqlite3
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT, jwt_required
from flask import Flask, request


class Item(Resource):
    parser = reqparse.RequestParser()  # get request parset and set arguments to it
    parser.add_argument('price',
                        type=float,
                        required=True,  # no req should come through without having price as attribute
                        help="This field cannot be left blank!"
                        )

    @jwt_required() #we will need to authenticate before this REQ can take place
    def get(self,name):
        item=self.find_item_by_name(name)
        if item:
            return item
        else:
            return {"message": "Item not found"}, 404


    @classmethod
    def find_item_by_name(cls,name):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        query="SELECT * FROM items WHERE name=?"
        result=cursor.execute(query,(name,))
        row=result.fetchone()
        connection.close()

        if row:
            return {'item':{'name':row[0], 'price':row[1]}}

    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()


    def post(self,name):
        if self.find_item_by_name(name):
            return {"message":"item with {} elready exists ".format(name)},400
        else:
            data=Item.parser.parse_args() #if JSON payload is not proper/body does not have JSON then this gives an err..to avoid err..use force
            item={'name':name, 'price':data['price']}

            try:
                self.insert(item)
            except:
                return {"message":"an error occured while posting"}, 500

            return item, 201


    def delete(self,name):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query="DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))

        connection.commit()
        connection.close()


    def put(self,name):
        #we don't want item name to get changed so we let only some arguments(price) to come through and filter using parser
        #parser belongs to class Item
        data=Item.parser.parse_args() #only arguments which we want will come through payload
        new_item = {'name': name, 'price': data['price']}

        item=self.find_item_by_name(name)
        if item is None:
            self.insert(new_item)
        else: #item exists so update it
            self.update(new_item)
        return new_item

    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'],item['name']))

        connection.commit()
        connection.close()



class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result=cursor.execute(query)

        connection.close()

        items = []

        for row in result:
            items.append({"name": row[0], "price": row[1]})

        return {"items":items}