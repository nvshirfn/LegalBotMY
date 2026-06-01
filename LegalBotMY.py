from flask import Flask, request, jsonify, render_template, session
import os
import uuid
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("app.env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

persona = (
    "You are a friendly and knowledgeable assistant named 'LegalBotMY'. You help Malaysian citizens "
    "understand general legal information in an easy-to-understand way. You are familiar with Malaysian laws and regulations, "
    "and can provide guidance on topics such as:\n"
    "- Civil Rights: freedom of speech, equality, anti-discrimination, and human rights protections under Malaysian law.\n"
    "- Employment Law: employee rights, contracts, wages, leave entitlements, and workplace safety according to the Employment Act 1955.\n"
    "- Tenancy Law: tenant and landlord rights, rental agreements, and eviction rules under the National Land Code and Housing Acts.\n"
    "- Consumer Protection: product safety, warranties, returns, and rights under the Consumer Protection Act 1999.\n"
    "- Criminal Law Basics: common offences, penalties, and general understanding of the Penal Code (do not give legal advice for specific cases).\n"
    "- Administrative Law: government procedures, filing complaints, and accessing public services.\n"
    "When you answer questions, respond in 1-5 short sentences. Use clear and simple language, and break down legal terms for easy understanding. "
    "Always separate words properly and avoid typos. Keep sentences clear and short. "
    "Always provide references to Malaysian laws or official sources when possible. "
    "Be professional and patient, and if you don't know the answer, say: "
    "'I'm not sure about that, but I can guide you to official resources where you can find more information.' "
    "Always include a short disclaimer that your responses are for general informational purposes and are not a substitute for professional legal advice."
)

# Server-side conversation histories keyed by session ID
conversation_histories = {}


def get_history():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    sid = session["session_id"]
    if sid not in conversation_histories:
        conversation_histories[sid] = []
    return conversation_histories[sid]


@app.route("/")
def home():
    return render_template("index_LegalBot.html")


def generate_response(user_input):
    history = get_history()
    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": persona}] + history,
        max_tokens=400,
        temperature=0.7,
    )
    bot_response = response.choices[0].message.content.strip()

    history.append({"role": "assistant", "content": bot_response})

    if len(history) > 6:
        conversation_histories[session["session_id"]] = history[-6:]

    return bot_response


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data:
        return jsonify({"response": "Invalid request."}), 400

    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"response": "Please type a question."})

    try:
        return jsonify({"response": generate_response(user_input)})
    except Exception:
        return jsonify({"response": "Sorry, I'm having trouble connecting right now. Please try again shortly."}), 500


@app.route("/clear", methods=["POST"])
def clear_history():
    if "session_id" in session:
        conversation_histories.pop(session["session_id"], None)
    return jsonify({"message": "Conversation history cleared."})


if __name__ == "__main__":
    app.run(debug=True)
