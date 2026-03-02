import telebot
from flask import Flask, request
import json
import os

TOKEN = "8232273708:AAHzvfCaEebwp0k9NDoRof93uKJnXWWHrsI"
ADMIN_ID = 7371121826

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

DATA_FILE = "data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {"books": {}, "users": []}

def save():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if user_id not in data["users"]:
        data["users"].append(user_id)
        save()

    args = message.text.split()

    # If deep link used
    if len(args) > 1:
        key = args[1]
        file_id = data["books"].get(key)

        if file_id:
            bot.send_document(message.chat.id, file_id)
        else:
            bot.send_message(message.chat.id, "❌ Invalid or expired link.")
        return

    # Premium Welcome
    bot.send_message(
        message.chat.id,
        "══════════════════════════════\n"
        "        🎓  𝐉𝐄𝐄 𝐓𝐑𝐀𝐂𝐊𝐄𝐑 𝐕𝐀𝐔𝐋𝐓  🎓\n"
        "══════════════════════════════\n\n"
        "Official Academic Resource Portal\n\n"
        "⚡ Instant PDF Delivery\n"
        "🔐 Unique Link System\n"
        "📂 Secure Digital Library\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📢 Backup:\n"
        "https://t.me/JEECBSENEETBOOKS\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )

# ---------------- ADD BOOK ----------------
@bot.message_handler(content_types=['document'])
def save_book(message):
    if message.from_user.id != ADMIN_ID:
        return

    if not message.caption:
        return

    key = message.caption
    file_id = message.document.file_id

    data["books"][key] = file_id
    save()

    bot_username = bot.get_me().username
    link = f"https://t.me/{bot_username}?start={key}"

    bot.reply_to(message, f"✅ Saved!\n\n🔗 Link:\n{link}")

# ---------------- STATS ----------------
@bot.message_handler(commands=['stats'])
def stats(message):
    if message.from_user.id != ADMIN_ID:
        return

    bot.reply_to(
        message,
        f"👥 Users: {len(data['users'])}\n"
        f"📚 Books: {len(data['books'])}"
    )

# ---------------- RUN ----------------
print("Bot Running...")
bot.infinity_polling()
