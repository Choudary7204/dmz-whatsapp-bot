from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")


@app.route("/")
def home():
    return "DMZ WhatsApp Bot is running!"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # Verification
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200

        return "Verification failed", 403

    # Incoming messages
    if request.method == "POST":
        data = request.get_json()

        try:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            sender = message["from"]

            send_message(sender, "Hello 👋 Welcome to DMZ AI Bot!")

        except Exception as e:
            print(e)

        return "OK", 200


def send_message(recipient, text):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {
            "body": text
        }
    }

    requests.post(url, headers=headers, json=payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
