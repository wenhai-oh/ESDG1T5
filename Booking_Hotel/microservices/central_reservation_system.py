from flask import Flask, request, jsonify, render_template, session, redirect
from flask_cors import CORS
from datetime import datetime, timedelta
from invokes import invoke_http
import random
import os, sys
import requests, json
import amqp_setup
import pika

app = Flask(__name__)
app.secret_key = 'esdg1t5' # for session
CORS(app)

product_manager_URL = os.environ.get('product_manager_URL') or "http://localhost:5001/product"
inventory_manager_URL = os.environ.get('inventory_manager_URL') or "http://localhost:5002/inventory"
reservation_manager_URL = os.environ.get('reservation_manager_URL') or "http://localhost:5003/reservation_manager"
customer_manager_URL = os.environ.get('customer_manager_URL') or "http://localhost:5004/customer_manager"
# notification_manager_URL = os.environ.get('notification_manager_URL') or "http://localhost:5005/notification"
refund_URL = os.environ.get('refund_URL') or "http://localhost:5005/refund"
payment_URL = os.environ.get('payment_URL') or "http://localhost:5006/payment"

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
@app.route("/send_otp", methods=["POST"])
def send_otp():
    reservationID = request.form['reservationID']
    # Get custID from Reservation Manager based on given reservationID.
    reservation = invoke_http(reservation_manager_URL +  "/" + str(reservationID), method="GET")
    custID = reservation['data']['custID']
    # Get customer name and email from Customer Manager based on custID.
    customer = invoke_http(customer_manager_URL +  "/" + str(custID), method="GET")
    customerName = customer['data']['name']
    customerEmail = customer['data']['email']
    # Generate random 6 digit OTP.
    otp = str(random.randint(100000, 999999))
    # Store the OTP and reservationID in a session variable to be used later by the verify_otp function.
    session['otp'] = otp
    session['reservationID'] = reservationID
    subject = "Your OTP for cancelling reservation"
    content = "Dear " + customerName + ",\n\nYour OTP is " + str(otp) + ".\n\nThank you."

    # Send OTP to customer email. (notification microservice)
    message = json.dumps({"customerEmail": customerEmail, "subject": subject, "content": content})
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notify", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2))
    
    # redirect webapge to enter otp
    # return render_template('http://localhost/ESDG1T5/Booking_Hotel/microservices/flask_stripe/flask_stripe/templates/verify_otp.html')
    return redirect('http://localhost/ESDG1T5/Booking_Hotel/microservices/flask_stripe/flask_stripe/templates/verify_otp.html')

@app.route('/crs/verify_otp', methods=['POST'])
def verify_otp():
    first = request.form['first']
    second = request.form['second']
    third = request.form['third']
    fourth = request.form['fourth']
    fifth = request.form['fifth']
    sixth = request.form['sixth']
    user_otp = str(first) + str(second) + str(third) + str(fourth) + str(fifth) + str(sixth)

    # Get the OTP and reservationID from the session variable
    otp = session['otp']
    reservationID = session['reservationID']
    # Verify the OTP entered by the user
    if user_otp == str(otp):
        # redirect to cancel_reservation function
        return redirect('http://localhost/ESDG1T5/Booking_Hotel/microservices/flask_stripe/flask_stripe/templates/Cancel_Reservation.html')
    else:
        return "OTP verification failed."
    
@app.route('/crs/cancel_reservation', methods=['POST'])
def cancel_reservation():
    reservationID = session['reservationID']
    reservation = invoke_http(reservation_manager_URL +  "/" + str(reservationID), method="GET")
    session_id = reservation['data']['session_id']
    refund = invoke_http(refund_URL +  "/" + str(session_id), method="POST")  
    reservation = invoke_http(reservation_manager_URL +  "/" + str(reservationID), method="DELETE")
    # get session_id from reservation manager
    session_id = reservation['data']['session_id']
    ## process refund.
    # get session_id from reservation manager
    return redirect('http://localhost/ESDG1T5/Booking_Hotel/microservices/flask_stripe/flask_stripe/templates/Checkinn_Index.html')
# ================ END Use Case 2: Customer Cancel Reservation ================

# ================ Use Case 3: Customer Make Payment for Room Reservation ================
@app.route("/crs/payment/<int:reservationID>", methods=["POST"])
def make_payment(reservationID):
    # Get custID, productID and quantity from Reservation Manager based on given reservationID.
    reservation = invoke_http(reservation_manager_URL +  "/" + str(reservationID), method="GET")
    custID = reservation['data']['custID']
    productID = reservation['data']['productID']
    quantity = reservation['data']['quantity']
    # Get customer name and email from Customer Manager based on custID.
    customer = invoke_http(customer_manager_URL +  "/" + str(custID), method="GET")
    customerName = customer['data']['name']
    customerEmail = customer['data']['email']

    # Get productRate from Product Manager based on productID.
    product = invoke_http(product_manager_URL +  "/id/" + str(productID), method="GET")
    productRate = product['data']['productRate']
    # Calculate total amount.
    totalAmount = productRate * quantity
    # Call payment microservice to make payment.


    # If payment is successful, send email to customer.
    subject = "Your payment for reservation"
    content = "Dear " + customerName + ",\n\nYour payment of $" + str(totalAmount) + " is successful.\n\nThank you."
    message = json.dumps({"customerEmail": customerEmail, "subject": subject, "content": content})
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notify", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2))

    # return output
    return jsonify({
        "data": totalAmount
        }), 200

# ================ END Use Case 3: Customer Make Payment for Room Reservation ================

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)