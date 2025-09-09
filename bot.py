from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "8357455905:AAGIR-0Zmd6xkk2GEislpKnguPyzWMEoi7U"  # التوكن هنا

async def reply_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await update.message.reply_text("مرحبا")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_hello))
    app.run_polling()

if __name__ == "__main__":
    main()