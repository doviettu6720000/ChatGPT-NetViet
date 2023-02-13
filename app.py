from flask import Flask, render_template, request, jsonify
import json
import openai

# from pyngrok import ngrok,conf

# url = ngrok.connect(5000).public_url
# conf.get_default().region = "us"

app = Flask(__name__, template_folder='templates') 

# print('Henzy Tunnel URL:', url)
# Define the API endpoint and API key
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
        max_tokens=3000,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    response_text = response.choices[0].text
    return response_text.strip()

# Serve the main HTML file
@app.route("/")
def index():
    return render_template("index.html")


# Handle the API request to send the message to the chatbot
@app.route("/send_message", methods=["POST"])
def send_message_api():
    if not request.is_json:
        return jsonify({"error": "Bad Request: request body must be a JSON object"}), 400

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Bad Request: request body must be a JSON object"}), 400

    message = data["message"]
    if message is None:
        return jsonify({"error": "Bad Request: missing 'message' key in the request body"}), 400

    response_message = send_message(message)
    print(response_message)
    return jsonify(message = response_message)

if __name__ == "__main__":
    app.run(debug=False)