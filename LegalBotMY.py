from flask import Flask, request, jsonify, render_template
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv("app.env")

# Initialize the OpenAI client with your API key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Initialize the Flask app
app = Flask(__name__)

# Comprehensive persona for LegalBotMY with a syllabus framework
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
    "Always separate words properly and avoid typos. Keep sentences clear and short."
    "Always provide references to Malaysian laws or official sources when possible. "
    "Be professional and patient, and if you don’t know the answer, say: "
    "'I’m not sure about that, but I can guide you to official resources where you can find more information.' "
    "Always include a short disclaimer that your responses are for general informational purposes and are not a substitute for professional legal advice."
)

# Conversation history to maintain context
conversation_history = []

# Flask route for the main page
@app.route("/")
def home():
    return render_template("index_LegalBot.html")

# Function to generate a response for the chatbot
def generate_response(user_input):
    global conversation_history
    conversation_history.append({"role": "user", "content": user_input})
    messages = [{"role": "system", "content": persona}] + conversation_history

    bot_response = ""
    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=50,
            temperature=0.7,
        )
        chunk = response.choices[0].message.content.strip()
        bot_response += chunk

        # If the chunk seems complete, break
        if chunk.endswith((".", "!", "?")):
            break

        # Add the partial response to the conversations to continue

        conversation_history.append({"role": "assistant", "content": chunk})
        messages = [{"role": "system", "content": persona}] + conversation_history

    conversation_history.append({"role": "assistant", "content": bot_response})

    # Limit the conversation history to avoid excessive context length
    if len(conversation_history) > 6:
        conversation_history = conversation_history[-6:]

    return bot_response

# Flask route for the chatbot API
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"response": "Please type a question."})

    return_text = generate_response(user_input)
    return jsonify({"response": return_text})


# Flask route to clear conversation history if needed
@app.route("/clear", methods=["POST"])
def clear_history():
    global conversation_history
    conversation_history = []
    return jsonify({"message": "Conversation history cleared."})

if __name__ == "__main__":
    app.run(debug=True)
