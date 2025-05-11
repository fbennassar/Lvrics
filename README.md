# Lyric Finder Bot

A Telegram bot for search song's lyrics using the lyrics.ovh API
 
## How to use

1.  Start bot in Telegram
2.  Usage: `/lyrics [artist] - [song] `

## Dependencies

-   python-telegram-bot
-   requests
-   python-dotenv

## Config

1.  Create a file `.env` and put your bot token and Genius access token:
    ```python
    TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
    GENIUS_TOKEN = "YOUR_GENIUS_ACCESS_TOKEN"
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Execute:
    ```bash
    python bot.py
    ```

## Telegram Bot

@LvricsBot
