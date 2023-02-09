import json
from flask import jsonify
import openai

# Load the API key from a JSON file
try:
    with open("apikey.json", "r") as f:
        data = json.load(f)
        api_key = data["key"]
except FileNotFoundError:
    print("Error: apikey.json file not found")
    api_key = None
except KeyError:
    print("Error: Invalid JSON file format")
    api_key = None

# Define the function to send the message to GPT-3
def send_message(message):
    if api_key is None:
        return "Error: API key not set"
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        max_tokens=100,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    response_text = response.choices[0].text
    return response_text.strip()

# Test the chatbot
while True:
    user_message = input("You: ")
    chatbot_response = send_message(user_message)
    print(f"Chatbot: {chatbot_response}")
    if user_message.strip().lower() == "q":
        break