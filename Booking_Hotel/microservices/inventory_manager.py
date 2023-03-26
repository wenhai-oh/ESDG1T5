from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Inventory Manager (date, productName, quantity)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)

class InventoryManager(db.Model):
    __tablename__ = "inventory_manager"

    date = db.Column(db.Date, primary_key=True)
    productName = db.Column(db.String(256), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, date, productName, quantity):
        self.date = date
        self.productName = productName
        self.quantity = quantity

    def json(self):
        return {
            "date": self.date,
            "productName": self.productName,
            "quantity": self.quantity,
        }

# Get all inventory items.
# Returns in the format of JSON.
@app.route("/inventory")
def get_all_inventory():
    inventoryList = InventoryManager.query.all()
    if len(inventoryList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "inventory": [inventory.json() for inventory in inventoryList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no inventory."
        }
    ), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)