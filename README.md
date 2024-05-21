## Telegram ATF Booru Scraper

This Python script scrapes media from a specified Booru site using its API and sends them to a Telegram channel. The script features:

- Downloading and sending images and videos to Telegram.
- Incremental scraping using pagination.
- Resuming progress from the last scraped page.
- Progress indicators during media sending.

### Requirements

- Python 3.6 or higher

You can install the required packages using pip:
```bash
pip install requests python-telegram-bot==13.7 tqdm
```

### Configuration

1. Obtain a [TELEGRAM BOT TOKEN](https://t.me/BotFather) and paste it into `TELEGRAM_TOKEN`.
2. Replace `CHAT_ID` with the your [CHAT ID](https://t.me/userinfobot).
3. Adjust `PAGE_LIMIT` to control the number of posts fetched per API request.

### Usage

1. Start the script: `python main.py`
2. In your Telegram channel, use the following commands:
    - `/start <tag>`: Start scraping media with the given tag from the first page.
    - `/continue <tag>`: Resume scraping with the given tag from the last saved page.

### Functionality

- **`/start <tag>`**: 
    - Resets the last scraped page to 1.
    - Starts fetching media from the specified Booru site for the given tag.
    - Sends each media item to your Telegram channel.
    - Saves the last scraped page number for resuming progress.

- **`/continue <tag>`**:
    - Reads the last saved page number.
    - Continues scraping from the last saved page for the given tag.
    - Sends each new media item to your Telegram channel.
    - Updates the last saved page number.

### Notes

- The script stores the last scraped page number in a file named `last_page.txt`. 
- Error handling is implemented to handle failed media downloads and API errors.
- Progress bars are displayed during media sending for better user experience.

### Disclaimer

This script is for educational purposes only. Please respect the terms and conditions of the Booru site you are scraping and use the script responsibly. Do not use it for any illegal or unauthorized activities. 
