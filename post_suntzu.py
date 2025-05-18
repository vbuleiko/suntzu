import telebot
import json
import os
import random
import re

TOKEN = '7756936525:AAEcuz3WziUnH3OrR0pkFpw1W2Nyg0rYFKI'
CHANNEL_ID = '@suntzu_vibe_vibe'
QUOTES_FILE = 'sun_tzu.json'
USED_FILE = 'sun_tzu_used.json'

def escape_markdown(text):
    """Экранирует спецсимволы для Markdown V2"""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

# Загрузка цитат
with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
    all_quotes = json.load(f)

if os.path.exists(USED_FILE):
    with open(USED_FILE, 'r', encoding='utf-8') as f:
        used_quotes = json.load(f)
else:
    used_quotes = []

used_texts = {q['quote'] for q in used_quotes}
unused_quotes = [q for q in all_quotes if q['quote'] not in used_texts]

if not unused_quotes:
    print("❗ Все цитаты использованы.")
    exit()

quote = random.choice(unused_quotes)

# Экранируем
quote_text = escape_markdown(quote['quote'])
source_text = escape_markdown(f"Сунь-цзы. {quote['source']}")

# Форматируем для MarkdownV2
formatted_text = f"_{quote_text}_\n\n*{source_text}*"

# Отправляем
bot = telebot.TeleBot(TOKEN, parse_mode="MarkdownV2")
bot.send_message(CHANNEL_ID, formatted_text)

# Обновляем список использованных
used_quotes.append(quote)
with open(USED_FILE, 'w', encoding='utf-8') as f:
    json.dump(used_quotes, f, ensure_ascii=False, indent=2)

print("✅ Отправлено!")
