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
    # Identify named entities

    recipient_number = None
    message = None
    for entity in doc.ents:
        print(entity.text, entity.label_)
        if entity.label_== "RECIPIENT_PHONE":
            recipient_number = entity.text
        if entity.label_== "MESSAGE":
            message = entity.text
    if not recipient_number:
        return "Receipient Number not present in message. Please resend."
    if not message:
        return "Couldn't understand what message you want to send. Please resend."

    send_message_return = send_message(recipient_number, message)
    print(send_message_return)
    return "I'm sorry, I couldn't understand your message. How can I assist you?"

def send_message(recipient, message):
    # Code for sending the message using Twilio

    print("In send message")
    print("Recepient phone number received as", recipient)

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
        return "Couldn't send message, please check your Twilio credentials."

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