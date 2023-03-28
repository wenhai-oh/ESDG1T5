from flask import Flask, render_template, url_for, request, abort
from flask_cors import CORS, cross_origin

import stripe

app = Flask(__name__)
CORS(app)

# Added Strip_Public_Key and Stripe_Secret_Key from Dashboard Developer. [TEST]
# Ignore yellow warnings - security issues cause secret key is hardcoded.
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51MqSh2HbqhyU3egayYvKbaPlW2sXFIKBUDJ5gXIztt4ADBLHECqufPM9TQ6aUxhFdBHDgqUAxJ9bOsrtY7laHK5C0059veyX9M'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51MqSh2HbqhyU3egaZux6oGJx38MGy0CAJdEyY0CiX2LjtZmrhZLrqem7yxSbkGP8545jcNHk14aCy0yHKcdWh2n900ElLKzUNc'


@app.route('/')
def index():
    return render_template(
        # Try add ./template or just /template
        'templates/Booking_Cart.html', 
        # checkout_session_id=session['id'], 
        # checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
    )

@app.route('/stripe_pay')
@cross_origin()
def stripe_pay():
    # print('hello')
    stripe.api_key = "sk_test_51MqSh2HbqhyU3egaZux6oGJx38MGy0CAJdEyY0CiX2LjtZmrhZLrqem7yxSbkGP8545jcNHk14aCy0yHKcdWh2n900ElLKzUNc"
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            # Added Product API ID which is created under product tabs.
            'price': 'price_1MqT0vHbqhyU3egaVAxDWtDy',
            'quantity': 1,
        }],
        # Added Automatic Tax Config from Stripe Doc -- Calculate Tax - Registered in Tax Registry.
        automatic_tax={
            'enabled': True
        },
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),

    )
    # Retrieve the Checkout Session object
    # session = stripe.checkout.Session.retrieve(session.id)
    # Access the Payment Intent ID associated with the Checkout Session
    # payment_intent_id = session['payment_intent']
    # print(payment_intent_id)
    print(session)

    return {
        # Change this line to paymentintentID instead.
        # Reason because checkout sessions will expire within an hour max, payment_intent_id doesn't expire, its associated or created whenever a checkout session is created.
        'checkout_session_id': session.id,
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

@app.route('template/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    # Need to change this via any stripe accounts changed
    endpoint_secret = 'whsec_LakNprCWo6aY0oR5Y2xtfMqHtfwKSx7n'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}

if __name__ == '__main__':
    app.run(port=5001, debug=True)