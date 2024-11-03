import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image
import pytesseract
import requests
from io import BytesIO

# Token bot dari BotFather
TOKEN = os.getenv('BOT_TOKEN')  # Mengambil token dari Environment Variables

# Variabel untuk menyimpan statistik
user_stats = {
    'total_images': 0,
    'total_texts': 0
}

# Fungsi untuk command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "Halo! Saya adalah bot🤖 Telegram.\n"
        "Anda dapat mengirim gambar🖼️ yang berisi teks, dan saya akan membantu membaca🔍 teks tersebut.\n"
        "Silakan kirimkan gambar🖼️ untuk memulai💥! Gunakan /help untuk melihat opsi lainnya."
    )
    await update.message.reply_text(welcome_message)

# Fungsi untuk menampilkan bantuan
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_message = (
        "Cara menggunakan bot ini:\n"
        "/start - Memulai bot\n"
        "/help - Menampilkan pesan ini\n"
        "Kirim gambar🖼️ untuk pemindaian🔍 teks."
    )
    await update.message.reply_text(help_message)

# Fungsi untuk merespon pesan teks
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Ketik /start untuk menjalankan bot dan memulai memindai gambar🔍.")

# Fungsi untuk mengubah gambar menjadi teks
async def image_to_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global user_stats
    if update.message.photo:
        user_stats['total_images'] += 1
        
        # Mengambil file foto dengan resolusi tertinggi
        photo_file = await update.message.photo[-1].get_file()
        photo_url = photo_file.file_path

        # Download gambar
        response = requests.get(photo_url)
        img = Image.open(BytesIO(response.content))

        # Lakukan OCR untuk membaca teks dari gambar
        await update.message.reply_text("Memindai gambar... Ini mungkin memerlukan beberapa saat. Silakan tunggu...")
        
        # Lakukan OCR untuk membaca teks dari gambar
        text = pytesseract.image_to_string(img)
        user_stats['total_texts'] += 1

        # Kirimkan hasil OCR ke pengguna
        await update.message.reply_text(f"SELESAI TUAN🥰:\n{text}")
    else:
        await update.message.reply_text("Silakan kirimkan gambar.")

# Fungsi untuk menampilkan statistik pengguna
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    stats_message = (
        f"Total gambar yang dipindai: {user_stats['total_images']}\n"
        f"Total teks yang diekstraksi: {user_stats['total_texts']}"
    )
    await update.message.reply_text(stats_message)

def main():
    # Membuat aplikasi bot dengan token
    application = Application.builder().token(TOKEN).build()

    # Menambahkan command handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats))

    # Menambahkan message handler untuk merespons semua teks yang masuk
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Menambahkan handler untuk gambar
    application.add_handler(MessageHandler(filters.PHOTO, image_to_text))

    # Menjalankan polling untuk menerima pesan
    application.run_polling()

if __name__ == '__main__':
    main()
