import spacy
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import spacy.cli

#spacy.cli.download("en_core_web_lg")

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

nlp1 = spacy.load("./model2/content/output/model-best") #load the best model

def generate_bot_response(user_message):
    doc = nlp1(user_message) # input sample text
    # Find named entities, phrases and concepts
    for entity in doc.ents:
        print(entity.text, entity.label_)
        if entity.label_== "RECIPIENT_PHONE":
            recipient_number = entity.text
        if entity.label_== "MESSAGE":
            message = entity.text
    send_message_return = send_message(recipient_number, message)
    print(send_message_return)
    return "I'm sorry, I couldn't understand your message. How can I assist you?"

def send_message(recipient, message):
    # Code for sending the message using Twilio

    print("In send message")
    print("Recepient phone number received as", recipient)

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

    return 

@app.route("/sms", methods=['POST'])
def sms_reply():
    data = request.get_json()
    user_message = data.get('Body')
    bot_response = generate_bot_response(user_message)
    response = MessagingResponse()
    response.message(bot_response)
    return jsonify(str(response))


if __name__ == "__main__":
    app.run(debug=True)