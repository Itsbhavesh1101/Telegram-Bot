# AI Joke Telegram Bot 🤖🎭

An AI-powered Telegram Bot that serves up witty, clean, and hilarious jokes on any topic you ask for! Built with Python, [python-telegram-bot](https://python-telegram-bot.org/), [LangChain](https://www.langchain.com/), and [Groq](https://groq.com/) (powered by the blazing-fast `Gemma2-9b-It` model).

## ✨ Features
- **Dynamic AI Jokes:** Generates unique jokes based on *any* provided topic.
- **Group & Private Chat Support:** 
  - **Private Chats:** Just type a topic to get a joke! No commands necessary.
  - **Groups:** Responds when mentioned (e.g., `@YourBotName dogs`).
- **Slash Commands:** Supports `/start`, `/help`, and `/joke <topic>` for straightforward usage.
- **Async Execution:** Utilizes asynchronous LangChain invocations to handle requests without blocking the bot.
- **Polished UI:** Displays a "🤔 Thinking..." message while the AI generates the joke, editing it seamlessly once ready.

## 🛠️ Tech Stack
- **Language:** Python 3.8+
- **Bot Framework:** `python-telegram-bot`
- **LLM Orchestration:** `LangChain`
- **LLM Provider:** `Groq API` (Model: `Gemma2-9b-It`)

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Itsbhavesh1101/Telegram-Bot.git
cd Telegram-Bot
```

### 2. Install Dependencies
Make sure you have Python installed. Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory (or use the one provided) and populate it with your API keys:

```env
# Required
TELEGRAM_API_KEY=your_telegram_bot_token_here
GROQ_API_KEY=your_groq_api_key_here

# Optional (for LangSmith Tracking/Debugging)
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_PROJECT=Telegram-Joke-Bot
```
> **How to get the keys?**
> - **Telegram Token:** Chat with [@BotFather](https://t.me/BotFather) on Telegram and create a new bot.
> - **Groq API Key:** Sign up on the [Groq Console](https://console.groq.com/) and generate an API key.

### 4. Run the Bot
Start the bot using Python:
```bash
python app.py
```
You should see `Bot is running...` in your terminal!

## 🎮 Usage
- **`/start`** - Get a friendly welcome message and instructions.
- **`/help`** - See how to use the bot.
- **`/joke <topic>`** - Get a joke on a specific topic.

*Enjoy the jokes and happy coding!* 🎉
