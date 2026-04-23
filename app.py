import os
import re
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()

# Set LangSmith environment variables safely
if os.getenv("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "Telegram-Joke-Bot")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"

def get_llm_chain():
    """Initializes and returns the LangChain model setup."""
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        logger.error("GROQ_API_KEY is not set in the environment variables.")
        return None

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a hilarious AI comedian. Give me only one funny joke about the provided topic. Keep it clean and witty."),
        ("user", "Topic: {topic}")
    ])
    
    llm = ChatGroq(
        model="gemma2-9b-it",
        groq_api_key=groq_api_key
    )
    
    return prompt | llm | StrOutputParser()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! \n\nI am your AI Joke Bot. \n"
        f"Send me a topic and I'll tell you a joke! \n\n"
        f"In groups, mention me like <code>@{context.bot.username} technology</code>\n"
        f"In private chats, just type the topic directly!"
    )
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "To use me, simply provide a topic you want a joke about.\n"
        "You can also use /joke <topic>."
    )

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /joke command."""
    if not context.args:
        await update.message.reply_text("Please provide a topic. Usage: /joke <topic>")
        return
    topic = " ".join(context.args)
    await generate_joke(update, context, topic)

async def generate_joke(update: Update, context: ContextTypes.DEFAULT_TYPE, topic: str):
    """Generates and sends a joke for the given topic."""
    chain = get_llm_chain()
    if not chain:
        await update.message.reply_text("Sorry, the bot is misconfigured (missing Groq API Key).")
        return

    # Send a temporary "thinking" message
    processing_msg = await update.message.reply_text(f"🤔 Thinking of a joke about: <b>{topic}</b>...", parse_mode="HTML")
    
    try:
        # Use ainvoke for asynchronous execution (non-blocking)
        joke = await chain.ainvoke({"topic": topic})
        joke = joke.strip()
        # Edit the thinking message with the joke
        await processing_msg.edit_text(joke)
    except Exception as e:
        logger.error(f"Error generating joke: {e}")
        await processing_msg.edit_text("Oops! My brain froze. Couldn't generate a joke right now.")
    
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages based on chat type."""
    msg = update.message.text
    chat_type = update.message.chat.type
    bot_username = context.bot.username
    
    # Check if it's a private chat
    if chat_type == "private":
        await generate_joke(update, context, msg.strip())
    else:
        # In groups, respond only if mentioned
        if f'@{bot_username}' in msg:
            # Extract topic after the bot username
            match = re.search(f'@{bot_username}\\s+(.*)', msg, re.IGNORECASE)
            if match and match.group(1).strip():
                await generate_joke(update, context, match.group(1).strip())
            else:
                await update.message.reply_text(f"Please provide a topic after my username. (e.g. @{bot_username} dogs)")

def main():
    """Start the bot."""
    token = os.getenv("TELEGRAM_API_KEY")
    if not token:
        logger.error("TELEGRAM_API_KEY is not set in the environment variables.")
        return

    app = Application.builder().token(token).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("joke", joke_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == "__main__":
    main()