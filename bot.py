"""Core"""
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
import lyrics_api

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Replace with your actual bot token


async def start(update, context):
    """Send a message when the command /start is issued."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello, World!")


async def hello(update, context):
    """Send a message when the command /hello is issued."""
    user = update.effective_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Hello, {user}!")

async def lyrics(update, context):
    """Fetch and send lyrics for a given artist and song."""
    if len(context.args) < 2:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Usage: /lyrics <artist> - <song>")
        return

    query = ' '.join(context.args)
    artist, song = query.split('-', 1)

    # Fetch lyrics using the lyrics_api module
    lyrics_text = lyrics_api.get_lyrics(artist, song)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=lyrics_text)

application = Application.builder().token(BOT_TOKEN).build()

start_handler = CommandHandler('start', start)
hello_handler = CommandHandler('hello', hello)
lyrics_handler = CommandHandler('lyrics', lyrics)

application.add_handler(start_handler)
application.add_handler(hello_handler)
application.add_handler(lyrics_handler)

application.run_polling()
