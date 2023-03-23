from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#create reservation manager - return CustID from ReservationID, delete reservation - return status, Reservation ID  return CustID and ProductID
#Reservation Manager (reservationID, custID, productID, status)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/reservation_manager"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)

class ReservationManager(db.Model):
    __tablename__ = "reservation_manager"

    reservationID = db.Column(db.Integer, primary_key=True)
    custID = db.Column(db.Integer, primary_key=True)
    productID = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(256), nullable=False)

    def __init__(self, reservationID, custID, productID, status):
        self.reservationID = reservationID
        self.custID = custID
        self.productID = productID
        self.status = status

    def json(self):
        return {
            "reservationID": self.reservationID,
            "custID": self.custID,
            "productID": self.productID,
            "status": self.status,
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
        # update the status of the reservation to "cancelled"
        reservation.status = "cancelled"
        db.session.commit()

        # delete the reservation from the database
        db.session.delete(reservation)
        db.session.commit()

        return jsonify(
            {
                "code": 200,
                "message": "Reservation with ID {} has been deleted and marked as cancelled.".format(reservationID)
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Reservation with ID {} not found.".format(reservationID)
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)