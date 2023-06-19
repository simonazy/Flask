from schemas import StoreSchema 
from db import stores 
from flask_smorest import Blueprint, abort 
from flask.views import MethodView 
import uuid 

blp = Blueprint("Stores", "stores", description="Operations on stores")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(cls):
        return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(cls, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store Already exists.")
        
        store_id = uuid.uuid4().hex 
        store = {**store_data, "id": store_id}
        stores[store_id] = store 

        return store 
    
# Endpoint is associated with the methodview class. 
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(cls, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(400, message="Store not found")

    def delete(cls, store_id):
        try:
            del stores[store_id]
            return {"message":"Store deleted."}
        except KeyError:
            abort(400, message="Store not found")