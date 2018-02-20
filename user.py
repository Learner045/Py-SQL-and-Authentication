import sqlite3
from flask_restful import Resource, reqparse
from flask import request

#this is an obj
class User:
    def __init__(self,_id,username,password):
        self.username=username
        self.password=password
        self.id=_id #id is a reserved word in python

    @classmethod #since we are not using self anywhere in our function
    def find_by_username(cls,username): #finding user from database
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query="SELECT * FROM users WHERE username=?"
        result = cursor.execute(query,(username,)) #parameter must be in the form of tupple
        row = result.fetchone()
        if row:
            user = cls(*row) #or use cls(*row)
        else:
            user = None
        connection.close() #V IMP
        return user

    @classmethod
    def find_by_userid(cls,_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select_query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(select_query,(_id,))  # parameter must be in the form of tupple
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2])  # or use cls(*row)
        else:
            user = None
        connection.close()  # V IMP
        return user

#this is a resource
class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                   type=str,
                   required=True,
                   help="this field cannot be empty",
    )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="this field cannot be empty",
                        )
    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            return {"message":"User with that username already exists"}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query="INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query,(data['username'],data['password']))

        connection.commit()
        connection.close()

        return {"message":"User registered successfully"}, 201


