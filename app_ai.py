import logging
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from transformers import pipeline

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/sms", methods=['POST'])
def sms_reply():
    data = request.get_json()
    user_message = data.get('Body')
    logger.info(f"Received message: {user_message}")
    bot_response = generate_bot_response(user_message)
    logger.info(f"Bot response: {bot_response}")
    response = MessagingResponse()
    response.message(bot_response)
    return str(response)

def generate_bot_response(user_message):

    print(user_message)
    if user_message is None:
        return "I'm sorry, I couldn't understand your message. How can I assist you?"

    nlp = pipeline("ner", model="distilbert-base-uncased", tokenizer="distilbert-base-uncased")
    entities = nlp(user_message)
    print(entities)

    recipient = None
    message_content = None

    for entity in entities:
        if entity['entity'] == 'PHONE':
            recipient = entity['word']
        elif entity['entity'] == 'PERSON':
            recipient = entity['word']
        elif entity['entity'] == 'MESSAGE':
            message_content = entity['word']

    if recipient and message_content:
        return send_message(recipient, message_content)

    return "I'm sorry, I couldn't understand your message. How can I assist you?"

def send_message(recipient, message):
    logger.info(f"Sending message to recipient: {recipient}")
    logger.info(f"Message content: {message}")
    # Replace this with your own implementation for sending the message
    return "Message sent successfully!"

if __name__ == "__main__":
    app.run(debug=True)
