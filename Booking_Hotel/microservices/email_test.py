from flask import Flask
from flask_mail import Mail, Message
import random

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'lokezhankang@gmail.com' # replace with your email address
app.config['MAIL_PASSWORD'] = 'pkewefqbhwwibywy' # replace with your email password
mail = Mail(app)

def generateOTP():
    return "".join(str(random.randint(1, 9)) for _ in range(6))

@app.route('/send_otp')
def send_otp():
    otp = generateOTP()
    msg = Message('Your One Time Password', sender = 'lokezhankang@gmail.com', recipients = ['lokezhankang@gmail.com']) # replace with the recipient's email address
    msg.body = f'Your OTP is {otp}.'
    mail.send(msg)
    return f'An OTP has been sent to your email. Your OTP is {otp}.'

if __name__ == '__main__':
    app.run(debug = True)