import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from yt_dlp import YoutubeDL

# Masukkan token bot Anda dari BotFather
TOKEN = "7913825794:AAHG18egVi2J85MXrF5dUCA5Izotjkxc6CE"

# Fungsi untuk mengatur opsi download video dan audio dengan cookies
def get_download_opts(download_type, quality):
    opts = {
        'cookiefile': 'cookies.txt',  # Menambahkan file cookies untuk autentikasi
    }
    if download_type == 'video':
        opts.update({
            'format': f'bestvideo[height<={quality}]+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s'
        })
    elif download_type == 'audio':
        opts.update({
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.mp3',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': quality}]
        })
    return opts

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Download Video", callback_data='choose_video_quality')],
        [InlineKeyboardButton("Download MP3", callback_data='choose_audio_quality')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Halo! Pilih opsi unduh di bawah ini:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'choose_video_quality':
        keyboard = [
            [InlineKeyboardButton("480p", callback_data='video_480')],
            [InlineKeyboardButton("720p", callback_data='video_720')],
            [InlineKeyboardButton("1080p", callback_data='video_1080')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Pilih resolusi video:", reply_markup=reply_markup)

    elif query.data == 'choose_audio_quality':
        keyboard = [
            [InlineKeyboardButton("64 kbps", callback_data='audio_64')],
            [InlineKeyboardButton("128 kbps", callback_data='audio_128')],
            [InlineKeyboardButton("192 kbps", callback_data='audio_192')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Pilih bitrate MP3:", reply_markup=reply_markup)

    elif query.data.startswith('video_') or query.data.startswith('audio_'):
        context.user_data['download_type'] = 'video' if query.data.startswith('video_') else 'audio'
        context.user_data['quality'] = query.data.split('_')[1]
        await query.edit_message_text("Silakan kirim tautan video yang ingin Anda unduh.")

async def download_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    download_type = context.user_data.get('download_type', 'video')
    quality = context.user_data.get('quality', '720')

    ydl_opts = get_download_opts(download_type, quality)
    await update.message.reply_text("Memulai unduhan, mohon tunggu...")

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

            # Kirim file sesuai tipe (audio/video)
            if download_type == 'audio':
                await update.message.reply_audio(audio=open(file_name, 'rb'))
            else:
                await update.message.reply_video(video=open(file_name, 'rb'))

            os.remove(file_name)  # Hapus file setelah dikirim
        except Exception as e:
            await update.message.reply_text(f"Kesalahan saat mengunduh: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Handler untuk perintah /start
    app.add_handler(CommandHandler("start", start))
    # Handler untuk tombol
    app.add_handler(CallbackQueryHandler(button_handler))
    # Handler untuk pesan URL
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_content))

    print("Bot downloader sedang berjalan...")
    app.run_polling()