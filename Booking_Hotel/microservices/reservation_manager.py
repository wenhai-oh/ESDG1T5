from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#create reservation manager - return CustID from ReservationID, delete reservation - return status, Reservation ID  return CustID and ProductID
#Reservation Manager (reservationID, custID, Startdate, EndDate productID, Quantity)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)

class ReservationManager(db.Model):
    __tablename__ = "reservation_manager"

    reservationID = db.Column(db.Integer, primary_key=True)
    custID = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.String(256),nullable=False)
    EndDate = db.Column(db.String(256),nullable=False)
    productID = db.Column(db.Integer, primary_key=True)
    Quantity = db.Column(db.Integer, primary_key=True)

    def __init__(self, reservationID, custID, StartDate, EndDate, productID, Quantity):
        self.reservationID = reservationID
        self.custID = custID
        self.StartDate = StartDate
        self.EndDate = EndDate
        self.productID = productID
        self.Quantity = Quantity

    def json(self):
        return {
            "reservationID": self.reservationID,
            "custID": self.custID,
            "startDate" : self.StartDate,
            "endDate" : self.EndDate,
            "productID": self.productID,
            "quantity": self.Quantity,
        }
      
# Retrive custID/ProductID/Status by reservationID
# Returns in the format of JSON.
@app.route("/reservation_manager/<int:reservationID>")
def find_by_reservationID(reservationID):
    reservation = ReservationManager.query.filter_by(reservationID=reservationID).first()
    if reservation:
        return jsonify(
            {
                "code": 200,
                "data": reservation.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Reservation with ID {} not found.".format(reservationID)
        }
    ), 404
  
#Delete Reservation/Change status to "cancelled"
@app.route("/reservation_manager/<int:reservationID>", methods=["DELETE"])
def delete_reservation(reservationID):
    reservation = ReservationManager.query.filter_by(reservationID=reservationID).first()
    if reservation:
        db.session.delete(reservation)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Reservation with ID {} has been cancelled.".format(reservationID)
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Reservation with ID {} not found.".format(reservationID)
        }
    ), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)
