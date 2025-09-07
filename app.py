import os
from flask import Flask, request, jsonify
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup

# تأكد من وضع توكن البوت كمتغير بيئة TELEGRAM_TOKEN
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("ضع متغير البيئة TELEGRAM_TOKEN مع توكن البوت")

bot = Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)

# التعامل مع الأزرار
def handle_callback(update: Update):
    query = update.callback_query
    query.answer()
    if query.data == "hello":
        query.edit_message_text("مرحباً! 👋 أنا هنا لمساعدتك.")
    elif query.data == "bye":
        query.edit_message_text("وداعاً! 👋 نراك قريباً.")

# التعامل مع /start
def handle_message(update: Update):
    msg = update.message
    keyboard = [
        [InlineKeyboardButton("قول مرحباً", callback_data='hello')],
        [InlineKeyboardButton("توديع", callback_data='bye')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg.reply_text("أنا مساعدك التجريبي! اختر زر:", reply_markup=reply_markup)

# webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    update_json = request.get_json(force=True)
    update = Update.de_json(update_json, bot)

    if update.callback_query:
        handle_callback(update)
    elif update.message:
        if update.message.text == "/start":
            handle_message(update)
        else:
            update.message.reply_text("أرسل /start لرؤية الأزرار.")

    return jsonify({"status": "ok"})

# health check
@app.route("/", methods=["GET"])
def index():
    return "بوت تليجرام التجريبي يعمل!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))