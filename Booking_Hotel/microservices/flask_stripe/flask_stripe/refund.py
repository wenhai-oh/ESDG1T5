import stripe
from flask import Flask, jsonify, request

app = Flask(__name__)
stripe.api_key = 'sk_test_51Mp7eaDR3XsfzYNcNN274W7Hmlsuvr7nDhtFN1UtuVH9dHVBRVVC9PRbhrL5BZ2SVEGfmoFEO8Z7CYr7BuxszJng00ScaMPkRp'

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
    
    return jsonify({'message': 'Refund Successful!'}), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)