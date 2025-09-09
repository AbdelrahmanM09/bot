import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "8357455905:AAGIR-0Zmd6xkk2GEislpKnguPyzWMEoi7U"
bot = Bot(token=TOKEN)

# Flask app
app = Flask(__name__)

# PTB Application
application = ApplicationBuilder().token(TOKEN).build()

# Handler: يرد مرحبا
async def reply_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await update.message.reply_text("مرحبا")

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_hello))

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "ok", 200

# Test endpoint
@app.route("/", methods=["GET"])
def index():
    return "Bot is running with Webhook!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
