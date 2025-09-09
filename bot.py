import os
import asyncio
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# إعداد اللوجز
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "8357455905:AAGIR-0Zmd6xkk2GEislpKnguPyzWMEoi7U"
bot = Bot(token=TOKEN)

app = Flask(__name__)

# PTB Application
application = ApplicationBuilder().token(TOKEN).build()

# Handler يرد مرحبا
async def reply_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received message from {update.effective_user.id}: {update.message.text}")
    if update.message and update.message.text:
        await update.message.reply_text("مرحبا")
        logger.info("Replied 'مرحبا' successfully.")

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_hello))

# Initialize و start PTB Application
asyncio.get_event_loop().run_until_complete(application.initialize())
asyncio.get_event_loop().run_until_complete(application.start())
logger.info("PTB Application initialized and started.")

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    logger.info("Incoming POST request from Telegram.")
    try:
        update_json = request.get_json(force=True)
        logger.info(f"Update JSON: {update_json}")
        update = Update.de_json(update_json, bot)
        asyncio.get_event_loop().create_task(application.process_update(update))
        return "ok", 200
    except Exception as e:
        logger.exception("Error processing update:")
        return "error", 500

# Test endpoint
@app.route("/", methods=["GET"])
def index():
    return "Bot is running with Webhook!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port)
