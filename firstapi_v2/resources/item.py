import uuid 
from flask.views import MethodView 
from flask_smorest import Blueprint, abort 
from db import stores, items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema) #When we use marshmallow for validation with Flask-Smorest, it will inject the validated data into our method for us.
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        for item in items.values():
            if (item_data["name"]==item["name"] 
                and item["store_id"]==item_data["store_id"]):
                abort(400, message=f"Item already exists.")
        item_id = uuid.uuid4().hex 
        item = {**item_data, "item_id":item_id}
        items[item_id] = item 

        return item 
    
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(400, message="Item not  found.")
        
    def delete(self, item_id):
        try:
            del(items[item_id])
            return {"message":"Item deleted"}
        except KeyError:
            abort(404, message="Item not found")
        
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data 
            return item 
        except KeyError:
            abort(404, message="Item not found.")






