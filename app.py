from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


@app.route("/")
def home():
    return "DMZ WhatsApp Bot is running!", 200


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # -------------------------------
    # VERIFY WEBHOOK
    # -------------------------------
    if request.method == "GET":

        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        print("Webhook Verification Request")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("Webhook Verified Successfully")
            return challenge, 200

        print("Verification Failed")
        return "Verification failed", 403

    # -------------------------------
    # RECEIVE MESSAGE
    # -------------------------------
    if request.method == "POST":

        try:

            data = request.get_json()

            print("====================================")
            print("Incoming Webhook")
            print(json.dumps(data, indent=2))
            print("====================================")

            value = data["entry"][0]["changes"][0]["value"]

            if "messages" not in value:
                print("No user message found.")
                return "EVENT_RECEIVED", 200

            message = value["messages"][0]

            sender = message["from"]

            if message.get("type") == "text":
                text = message["text"]["body"]
            else:
                text = ""

            print("Sender :", sender)
            print("Message:", text)

            reply = (
                "Hi 👋\n\n"
                "Welcome to DataMentorZen 🚀\n\n"
                "Please share the following details:\n\n"
                "1️⃣ Name\n"
                "2️⃣ Email ID\n"
                "3️⃣ Place\n"
                "4️⃣ Student / Working Professional\n"
                "5️⃣ Current Course / Domain"
            )

            url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": sender,
                "type": "text",
                "text": {
                    "body": reply
                }
            }

            response = requests.post(
                url,
                headers=headers,
                json=payload
            )

            print("WhatsApp API Status :", response.status_code)
            print("WhatsApp API Response :", response.text)

        except Exception as e:

            print("====================================")
            print("ERROR OCCURRED")
            print(str(e))
            print("====================================")

        return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
