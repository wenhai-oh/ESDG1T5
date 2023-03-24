from flask import Flask, render_template, url_for, request, abort
from flask_cors import CORS, cross_origin

import stripe

app = Flask(__name__)
CORS(app)

# Added Strip_Public_Key and Stripe_Secret_Key from Dashboard Developer. [TEST]
# Ignore yellow warnings - security issues cause secret key is hardcoded.
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51Mp7eaDR3XsfzYNcPVimPRsWOP3xN2elpvGPv2yI1bq1DnBv8TZysOvfu3XIuuYDekgCNIlcPCbW7A6BWOBCgaOo00uW60aXX5'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51Mp7eaDR3XsfzYNcNN274W7Hmlsuvr7nDhtFN1UtuVH9dHVBRVVC9PRbhrL5BZ2SVEGfmoFEO8Z7CYr7BuxszJng00ScaMPkRp'


@app.route('/')
def index():
    return render_template(
        'index.html', 
        # checkout_session_id=session['id'], 
        # checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
    )

@app.route('/stripe_pay')
@cross_origin()
def stripe_pay():
    stripe.api_key = "sk_test_51Mp7eaDR3XsfzYNcNN274W7Hmlsuvr7nDhtFN1UtuVH9dHVBRVVC9PRbhrL5BZ2SVEGfmoFEO8Z7CYr7BuxszJng00ScaMPkRp"
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            # Added Product API ID which is created under product tabs.
            'price': 'price_1MpBteDR3XsfzYNcAahtVWmV',
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
    print(session)

    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

@app.route('/thanks')
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
    endpoint_secret = 'YOUR_ENDPOINT_SECRET'
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
    app.run(port=5800, debug=True)