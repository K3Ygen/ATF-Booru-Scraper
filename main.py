import requests
import os
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from tqdm import tqdm

# Configuration
API_URL = "https://booru.allthefallen.moe"  # ATF Booru site URL
TELEGRAM_TOKEN = "TELEGRAM_TOKEN"  # Retrieve from environment variable
CHAT_ID = "CHAT_ID"  # Retrieve from environment variable
PAGE_LIMIT = 10000  # change if you wish
STATE_FILE = "last_page.txt"

error_count = 0

# --- Functions ---

def read_last_page():
    """Reads the last processed page from the state file."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as file:
            return int(file.read().strip())
    return 1

def write_last_page(page):
    """Writes the current page to the state file."""
    with open(STATE_FILE, "w") as file:
        file.write(str(page))

def search_media(tag: str, bot: Bot, start_page: int):
    """Searches for media with a given tag and sends them to Telegram."""
    global error_count  # Make sure to access the global error_count
    page = start_page
    while True:
        url = f"{API_URL}/posts.json"
        params = {
            "tags": tag,
            "limit": PAGE_LIMIT,
            "page": page
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if not data:
                break  # Stop if no more data
            bot.send_message(chat_id=CHAT_ID, text=f"Processing page {page}")
            send_to_telegram(bot, data)
            write_last_page(page)
            page += 1
        else:
            print(f"Error: {response.status_code}")
            break

def send_to_telegram(bot: Bot, media_list: list):
    """Sends a list of media items to the specified Telegram chat."""
    global error_count
    for media in tqdm(media_list, desc="Sending media"):
        if 'file_url' in media:
            file_url = media['file_url']
            post_url = f"{API_URL}/posts/{media['id']}"
            try:
                if file_url.endswith(('mp4', 'mov', 'avi', 'mkv', 'webm')):
                    bot.send_video(chat_id=CHAT_ID, video=file_url)
                else:
                    bot.send_photo(chat_id=CHAT_ID, photo=file_url)
            except Exception as e:
                error_count += 1
                print(f"Failed to send media: {e}, Error count: {error_count}")
                bot.send_message(chat_id=CHAT_ID, text=f"Failed to load media: {post_url}, Error count: {error_count}")
        else:
            print("No file_url found in media item")

# --- Telegram Bot Commands ---

def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command, starts a new search."""
    args = context.args
    last_page = read_last_page()

    if not args:
        update.message.reply_text(
            f"Do you want to continue from page {last_page}? Use /continue to continue or /start <tag> to start with a new tag."
        )
        return

    tag = ' '.join(args)
    write_last_page(1)  # Reset last page when starting new tag
    search_media(tag, context.bot, 1)

def continue_command(update: Update, context: CallbackContext) -> None:
    """Handles the /continue command, resumes from the last page."""
    args = context.args
    if not args:
        update.message.reply_text('Please provide a tag. Usage: /continue <tag>')
        return

    tag = ' '.join(args)
    last_page = read_last_page()
    search_media(tag, context.bot, last_page)

# --- Main ---

def main():
    """Starts the Telegram bot and sets up the command handlers."""
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("continue", continue_command))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
