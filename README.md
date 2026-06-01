# LegalBotMY ⚖️

An AI-powered chatbot that helps Malaysian citizens understand general legal information in simple, plain language.

## Features

- Covers key areas of Malaysian law:
  - Civil Rights
  - Employment Law (Employment Act 1955)
  - Tenancy Law (National Land Code & Housing Acts)
  - Consumer Protection (Consumer Protection Act 1999)
  - Criminal Law Basics (Penal Code)
  - Administrative Law
- Maintains per-user conversation context across a session
- Responses capped at 1–5 complete sentences for clarity
- Quick-action buttons for common legal questions
- Typing indicator and timestamped messages
- Clear conversation history option

## Tech Stack

- **Backend:** Python, Flask
- **AI:** OpenAI GPT-4o-mini
- **Frontend:** HTML, CSS, JavaScript
- **Environment:** python-dotenv

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Cikgu_Bot.git
cd Cikgu_Bot
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create an `app.env` file in the project root:

```
OPENAI_API_KEY=your-openai-api-key-here
SECRET_KEY=your-secret-key-here
```

> Get your OpenAI API key from [platform.openai.com](https://platform.openai.com).  
> You can generate a secure secret key with: `python -c "import secrets; print(secrets.token_hex(32))"`

### 5. Run the app

```bash
python LegalBotMY.py
```

Then open your browser at `http://127.0.0.1:5000`.

## Project Structure

```
Cikgu_Bot/
├── LegalBotMY.py           # Flask app and chatbot logic
├── requirements.txt        # Python dependencies
├── app.env                 # Environment variables (not committed)
└── templates/
    └── index_LegalBot.html # Frontend UI
```

## Disclaimer

LegalBotMY provides **general information only** and is **not a substitute for professional legal advice**. Always consult a qualified lawyer for advice specific to your situation.
