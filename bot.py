"""Core"""
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import apis.lyrics_api as lyrics_api
import apis.genius_api as genius_api

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Replace with your actual bot token
# Replace with your actual Genius API token
GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")


async def start(update, context):
    """Send a message when the command /start is issued."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="""Hi! I'm a bot that can help you find song lyrics.
        Use /help to see what I can do.""")


async def help_command(update, context):
    """Send a message when the command /help is issued."""
    user = update.effective_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"""Hello, {user}!
        I am a bot that can help you find song lyrics. Use "/lyrics [song's name]" to get started.
        And if you want to know more about me, 
        go to my repository: https://github.com/fbennassar/Lvrics.git""")


async def lyrics(update, context):
    """Fetch and send specific song and artist from Genius."""
    items = genius_api.get_genius_list(context.args, GENIUS_TOKEN)
    keyboard = []

    for idx, item in enumerate(items):
        # Limitar el texto del botón a 64 caracteres ya que Telegram no permite más
        keyboard.append([InlineKeyboardButton(item, callback_data=str(idx))])
    context.user_data['items'] = items  # Guardar los items en user_data
    print(keyboard)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Choose a song:",
        reply_markup=reply_markup
    )


async def button_callback(update, context):
    """Handle button callback from InlineKeyboard."""
    query = update.callback_query
    await query.answer()  # Responde al callback para evitar errores en Telegram

    idx = int(query.data)
    # print(f"Index: {idx}")
    items = context.user_data.get("items", [])
    # print(f"Items: {items}")
    if 0 <= idx < len(items):
        selected_option = items[idx]
        song, artist = selected_option.split(' - ', 1)
        lyrics_text = lyrics_api.get_lyrics(artist, song)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=lyrics_text
        )
    else:
        await query.edit_message_text(text="Selección inválida.")

# Agregar el CallbackQueryHandler al bot

application = Application.builder().token(BOT_TOKEN).build()


start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help_command)
lyrics_handler = CommandHandler('lyrics', lyrics)

application.add_handler(start_handler)
application.add_handler(help_handler)
application.add_handler(lyrics_handler)
application.add_handler(CallbackQueryHandler(button_callback))

application.run_polling()
