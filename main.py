import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Masukkan token bot Anda dari BotFather
TOKEN = 'YOUR_BOT_TOKEN_HERE'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Halo! Saya adalah bot sederhana.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ini adalah bot sederhana. Kirim /start untuk memulai.')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot sedang berjalan...")
    app.run_polling()
