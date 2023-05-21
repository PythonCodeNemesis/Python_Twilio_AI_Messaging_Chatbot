from transformers import pipeline

def extract_message_and_phone_number(input_sentence):
    nlp = pipeline("ner", model="distilbert-base-uncased", tokenizer="distilbert-base-uncased")
    entities = nlp(input_sentence)
    
    message = ""
    phone_number = ""
    
    for entity in entities:
        if entity['entity'] == 'MESSAGE':
            message += entity['word'] + " "
        elif entity['entity'] == 'PHONE':
            phone_number += entity['word']
    
    return message.strip(), phone_number

# Example usage
input_sentence = "Please send a text to +1234567890 with the message: Hello there!"
message, phone_number = extract_message_and_phone_number(input_sentence)
print("Message:", message)
print("Phone number:", phone_number)
