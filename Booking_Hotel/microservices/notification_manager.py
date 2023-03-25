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

#Send email through rabbitmq(ampq) server
import pika
import json

# RabbitMQ server settings
RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
RABBITMQ_QUEUE = "email_queue"

# function to send email
#email and email_content(OTP) are inputs provided by the CRS
def send_email(email, email_content):
    # connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=pika.PlainCredentials(
            RABBITMQ_USER, RABBITMQ_PASSWORD)))
    
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_QUEUE)

    # create the email message
    email_message = {
        "to": email,
        "subject": "Notification Email",
        "content": email_content
    }

    # convert the email message to JSON
    email_message_json = json.dumps(email_message)

    # publish the email message to the queue
    channel.basic_publish(exchange="", routing_key=RABBITMQ_QUEUE, body=email_message_json)

    # close the connection
    connection.close()

# route to send email
@app.route("/send_email", methods=["POST"])
def send_email_route():
    email = request.form.get("email_address")
    email_content = request.form.get("email_content")
    send_email(email, email_content)
    return jsonify({"message": "Email sent successfully"})
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
