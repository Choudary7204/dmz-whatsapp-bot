from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


@app.route("/")
def home():
    return "DMZ WhatsApp Bot is running!"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # Verify webhook
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200

        return "Verification failed", 403

    # Receive messages
    if request.method == "POST":
        data = request.get_json()
        print("Incoming data:", data)

        try:
            value = data["entry"][0]["changes"][0]["value"]

            if "messages" in value:

                sender = value["messages"][0]["from"]
                text = value["messages"][0]["text"]["body"]

                print("Sender:", sender)
                print("Message:", text)

                reply = (
                    "Hi 👋\n\n"
                    "Thanks for contacting DataMentorZen 🚀\n\n"
                    "Before we guide you further, please share:\n\n"
                    "1️⃣ Name\n"
                    "2️⃣ Email ID\n"
                    "3️⃣ Place\n"
                    "4️⃣ Student / Working Professional\n"
                    "5️⃣ Current course / field"
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

                print("Status Code:", response.status_code)
                print("Response:", response.text)

        except Exception as e:
            print("ERROR:", str(e))

        return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
