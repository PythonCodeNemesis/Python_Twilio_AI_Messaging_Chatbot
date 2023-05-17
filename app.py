from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ne_chunk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('maxent_ne_chunker')
nltk.download('words')

app = Flask(__name__)

def generate_bot_response(user_message):
    tokens = word_tokenize(user_message.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    ner_tags = ne_chunk(nltk.pos_tag(filtered_tokens))

    for chunk in ner_tags:
        if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
            recipient = ' '.join(c[0] for c in chunk.leaves())
            return send_message(recipient, user_message)

    return "I'm sorry, I couldn't understand your message. How can I assist you?"

def send_message(recipient, message):
    # Code for sending the message using Twilio
    # Replace this with your own Twilio implementation

    # Here's a sample implementation using the Twilio Python SDK
    from twilio.rest import Client

    # Twilio account credentials
    account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    twilio_phone_number = 'YOUR_TWILIO_PHONE_NUMBER'

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Send the message using Twilio
    try:
        message = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=recipient
        )
        return f"Message sent to {recipient} successfully!"
    except Exception as e:
        return f"Failed to send message: {str(e)}"

@app.route("/sms", methods=['POST'])
def sms_reply():
    user_message = request.form.get('Body')
    bot_response = generate_bot_response(user_message)
    response = MessagingResponse()
    response.message(bot_response)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
