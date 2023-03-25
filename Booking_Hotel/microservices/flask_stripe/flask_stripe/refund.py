import stripe
from flask import Flask, jsonify, request

app = Flask(__name__)
stripe.api_key = 'YOUR_STRIPE_SECRET_KEY'

@app.route('/refund', methods=['POST'])
def create_refund():
    session_id = request.json['session_id']
    
    # Retrieve the session
    session = stripe.checkout.Session.retrieve(session_id)
    
    # Get the payment intent ID from the session
    payment_intent_id = session['payment_intent']
    
    # Create the refund
    refund = stripe.Refund.create(
        payment_intent=payment_intent_id
    )
    
    return jsonify(refund), 200

if __name__ == '__main__':
    app.run(port=5800, debug=True)