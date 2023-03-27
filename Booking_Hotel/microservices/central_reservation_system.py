from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

import os
import sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

product_manager_URL = os.environ.get('product_manager_URL') or "http://localhost:5001/product"
inventory_manager_URL = os.environ.get('inventory_manager_URL') or "http://localhost:5002/inventory"
reservation_manager_URL = "http://localhost:5003/reservation_manager"
customer_manager_URL = "http://localhost:5004/customer_manager"
notification_URL = "http://localhost:5005/notification"
payment_URL = "http://localhost:5006/payment"

# Database Tables:
# Customer Manager (CustID, Name, Gender, Email)
# Product Manager (productID, productName, images, productRate)
# Inventory Manager (date, productName, quantity)
# Reservation Manager (reservationID, custID, StartDate, EndDate, productID, Quantity)

# ================ Use Case 1: Customer Browse Available Rooms ================
# Get available rooms based on dates [fromDate, toDate].
@app.route("/crs/<string:fromDate>/<string:toDate>")
def list_rooms(fromDate, toDate):
    # Initialise list of productName and dateList within the dates specified for room reservation.
    returnDict = {}
    productNameList = ["Single Room", "Double Room", "Suite"]
    dateList = [] # ["2023-03-11", "2023-03-12", ...]
    
    # populate dateList.
    currDate = datetime.strptime(fromDate, '%Y-%m-%d').date()
    toDate = datetime.strptime(toDate, '%Y-%m-%d').date()
    while currDate <= toDate:
        dateList.append(str(currDate))
        currDate += timedelta(days=1)

    for date in dateList:
        productsDict = {} # {productName: {quantity: 0, productRate: 0}, ...}
        for productName in productNameList:
            productDetail = {} # {quantity: 0, productRate: 0
            productName = productName.replace(" ", "%20")
            
            # Get data from Inventory Manager based on (date and productName).
            inventory = invoke_http(inventory_manager_URL +  "/" + date + "/" + productName, method="GET")

            # link productName and ProductRate.
            if "data" in inventory:
                # Get data from Product Manager based on (productName).
                product = invoke_http(product_manager_URL +  "/" + productName, method="GET")
                productName = inventory["data"]["inventory"][0]["productName"].replace("%20", " ")
                quantity = inventory["data"]["inventory"][0]["quantity"]
                productRate = product["data"]["productRate"]

                # Append to productList.
                productDetail = {
                        "quantity": quantity,
                        "productRate": productRate
                    }
                productsDict[productName] = productDetail
        # Append to returnList if date has results.
        if productsDict != {}:
            returnDict[date] = productsDict

    if returnDict == {}:
        return jsonify({
            "code": 404,
            "message": "No available rooms."
        }), 404
    
    return jsonify({
        "code": 200,
        "data": returnDict
    }), 200
# ================ END Use Case 1: Customer Browse Available Rooms ================


# ================ Use Case 2: Customer Cancel Reservation ================
# Get custID from Reservation Manager based on given reservationID.
# Get customer name and email from Customer Manager based on custID.
# Generate random 6 digit OTP.
# Send OTP to customer email. (notification microservice)
# Customer enters OTP. Verify OTP.
# If OTP is correct, delete reservation (reservationID) from Reservation Manager.
@app.route("/crs/<int:reservationID>", methods=["DELETE"])
def cancel_reservation(reservationID):
    # wait for reservation microservice.
    a = 1
# ================ END Use Case 2: Customer Cancel Reservation ================

# ================ Use Case 3: Customer Make Payment for Room Reservation ================
# ...

# ================ END Use Case 3: Customer Make Payment for Room Reservation ================

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)