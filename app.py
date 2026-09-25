from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create the flask application
app = Flask(__name__)

chatbot = Chatbot(
    "StudentBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///chatbot_database.sqlite3",
)

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", method=[POST])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"response": "Please enter a message!"})

    if len(user_message) > 500:
        return jsonify(
            {"response": "Message too long! Please keep it under 500 characters."}
        )

    # Get the chatbot's response
    bot_response = chatbot.get_response(user_message)

    return jsonify({"response": str(bot_response)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
