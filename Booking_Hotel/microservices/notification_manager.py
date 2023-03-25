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
