import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "8357455905:AAGIR-0Zmd6xkk2GEislpKnguPyzWMEoi7U"
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Application PTB
application = ApplicationBuilder().token(TOKEN).build()

# Handler: يرد "مرحبا"
async def reply_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await update.message.reply_text("مرحبا")

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_hello))

# Initialize PTB application (async)
asyncio.get_event_loop().run_until_complete(application.initialize())
asyncio.get_event_loop().run_until_complete(application.start())

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    # نشغل الـ handler مباشرة
    asyncio.get_event_loop().create_task(application.process_update(update))
    return "ok", 200

# Test endpoint
@app.route("/", methods=["GET"])
def index():
    return "Bot is running with Webhook!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
