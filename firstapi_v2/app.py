from flask import Flask, request
from db import items, stores
from flask_smorest import Api
import uuid

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

app = Flask(__name__)

app.config["PROPAGATE EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api=Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)

# #first endpoint: will return the data when the client request it. 
# @app.get("/store")   #http://127.0.0.1:5000/store
# def get_stores():
#     return {"stores": list(stores.values())}

# # What is JSON? 
# # JSON is a STRING whose contents follow a spcific format. 

# @app.post("/store")
# def create_store():  #view function: as they are called, they need to return something
#     store_data = request.get_json()
#     store_id =uuid.uuid4().hex
#     store = {**store_data, "id":store_id}
#     stores[store_id] = store
#     return stores, 201

# # pass query string paramater: http://127.0.0.1:5000/store?name=My Store
# @app.post("/item")
# def create_item(name):
#     item_data = request.get_json()
#     if item_data["store_id"] not in stores:
#         abort(404, message="Store not found")
#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id":item_id}
#     items[item_id] = item 
     
#     return items, 201
    

# @app.get("/store/<string:store_id>")
# def get_store(name):
#     try:
#         return stores["store_id"] 
#     except KeyError:
#         return {"message":"Store not found"}, 404 

# @app.get("/item")
# def get_all_items():
#     return {"items": list(items.values())}, 404


# @app.get_item("/item/<string:item_id>")
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         return {"message":"Item not found"}, 404 
    


