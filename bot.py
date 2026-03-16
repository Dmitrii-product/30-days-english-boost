import json
import random
import asyncio
from telegram import Bot
import os

# Now the script looks for the variables in the GitHub environment
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


async def send_daily_word():
    # 1. Load the words from your JSON file
    with open('words.json', 'r') as f:
        words = json.load(f)

    # 2. Pick a random word
    entry = random.choice(words)

    # 3. Format the message with Markdown
    message = (
        f"🌟 *C1 Word of the Day: {entry['word']}*\n\n"
        f"📚 *Definition:* {entry['definition']}\n\n"
        f"📝 *Example:* _{entry['example']}_\n\n"
        f"--- \n"
        f"💪 *Stress Test:* Can you use '{entry['word'].lower()}' in a sentence about your current project?"
    )

    # 4. Send the message
    bot = Bot(token=TOKEN)
    async with bot:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
        print(f"Sent: {entry['word']}")

if __name__ == "__main__":
    asyncio.run(send_daily_word())