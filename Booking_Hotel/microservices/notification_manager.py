from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# from notification_manager import NotificationManager

# Notification Manager ()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/notification_manager"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)

#Generate random OTP for input CustID and email from CRS
@app.route("/notification_manager/generate_otp", methods=["POST"])
def generate_otp():
    custID = request.json.get("custID")
    email = request.json.get("email")

    # Generate a 6-digit OTP
    otp = random.randint(100000, 999999)

    # TODO: Send the OTP to the email address using a third-party library or service

    return jsonify(
        {
            "code": 200,
            "data": {
                "custID": custID,
                "email": email,
                "otp": otp,
            },
            "message": "OTP generated successfully."
        }
    )
if __name__ == '__main__':
    app.run(port=5000, debug=True)

#code to be removed
"""
class NotificationManager(db.Model):
    __tablename__ = "notification_manager"

    notificationID = db.Column(db.Integer, primary_key=True)
    custID = db.Column(db.Integer, primary_key=True)
    productID = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(256), nullable=False)

    def __init__(self, notificationID, custID, productID, status):
        self.notificationID = notificationID
        self.custID = custID
        self.productID = productID
        self.status = status

    def json(self):
        return {
            "notificationID": self.notificationID,
            "custID": self.custID,
            "productID": self.productID,
            "status": self.status,
        }
      
# Retrive custID/ProductID/Status by notificationID
# Returns in the format of JSON.
@app.route("/notification_manager/<int:notificationID>")
def find_by_notificationID(notificationID):
    notification = NotificationManager.query.filter_by(notificationID=notificationID).first()
    if notification:
        return jsonify(
            {
                "code": 200,
                "data": notification.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "notification with ID {} not found.".format(notificationID)
        }
    ), 404
  
#Delete notification/Change status to "cancelled"
@app.route("/notification_manager/<int:notificationID>", methods=["DELETE"])
def delete_notification(notificationID):
    notification = NotificationManager.query.filter_by(notificationID=notificationID).first()
    if notification:
        # update the status of the notification to "cancelled"
        notification.status = "cancelled"
        db.session.commit()

        # delete the notification from the database
        db.session.delete(notification)
        db.session.commit()

        return jsonify(
            {
                "code": 200,
                "message": "notification with ID {} has been deleted and marked as cancelled.".format(notificationID)
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Notification with ID {} not found.".format(notificationID)
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
"""
