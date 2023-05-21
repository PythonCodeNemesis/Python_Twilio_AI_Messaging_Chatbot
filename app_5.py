import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ne_chunk, pos_tag

from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import ne_chunk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('maxent_ne_chunker')
nltk.download('words')

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def generate_bot_response(user_message):
    print("In generate bot response")
    print(user_message)

    if user_message is None:
        return "I'm sorry, I couldn't understand your message. How can I assist you?"

    tokens = word_tokenize(user_message.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    ner_tags = ne_chunk(pos_tag(filtered_tokens))
    print(ner_tags)

    recipient = None
    message_content = None

    for chunk in ner_tags:
        if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
            recipient = ' '.join(c[0] for c in chunk.leaves())
            #break

        recipient_phone = extract_phone_number(chunk)
        if recipient_phone:
            recipient = recipient_phone

    print("receipients number", recipient_phone)
    print("receipeint is", recipient)

    message_content = extract_message_content(user_message)
    
    if recipient and message_content:
        return send_message(recipient_phone, message_content)

    return "I'm sorry, I couldn't understand your message. How can I assist you?"

def extract_phone_number(chunk):
    # Extract the phone number from the chunk
    phone_number = None
    for c in chunk.leaves():
        if c[1] == 'CD':  # CD represents cardinal number, which is often used for phone numbers
            phone_number = c[0]
            break
    return phone_number

def send_message(recipient, message):
    # Code for sending the message using Twilio
    # Replace this with your own Twilio implementation

    print("In send message")
    print("Recipient phone number received as", recipient)

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

def extract_message_content(user_message):
    # Extract the content of the message between "message:" and "to:" (if present)

    print("In extract message content")
    start_index = user_message.find("message:")
    if start_index != -1:
        content = user_message[start_index + len("message:"):].strip()
        print("content", content)
        return content
    else:
        print("content", content)
        return ""


@app.route("/sms", methods=['POST'])
def sms_reply():
    data = request.get_json()
    user_message = data.get('Body')
    bot_response = generate_bot_response(user_message)
    response = MessagingResponse()
    response.message(bot_response)
    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
