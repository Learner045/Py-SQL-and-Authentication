from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from Authentication.item import Item, ItemList
from Authentication.security import authenticate, identity
from Authentication.user import UserRegister

app=Flask(__name__)
app.secret_key='jose'
api=Api(app)

jwt=JWT(app,authenticate,identity)
#creates a new endpoint /auth ..request sens us username,pass..which is send to authenticate()
#auth endpoint  then returns  a JWT token, this token is then used for identification purpose of user
#identity() method is used to check if userid matches


#http status codes:
#  200-ohk data returned successfully  404-not found
# 201-data created
# 202-accepted, when creation of obj is delayed and is done after latency behind the scnees
#500 internal server err

api.add_resource(Item, '/item/<string:name>') #we are receiving name directly from url into our method
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister,'/register')


#this file will only be considered main file if we are directly running it.
# But if it is just imported into another file and another file is run, then app file won't run along with it
#If we have just imported this file elsewhere then we don't want to run the flask app
if __name__=='__main__':
    app.run(port=5000, debug=True)


