import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from threading import Timer

# Inisialisasi logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Token API bot
TOKEN = '7285279612:AAFASwTDva5PXZ-CaKRm_ni8j9sSRhLTS9Y'  # Ganti dengan token bot Anda

# Global timer
countdown_timer = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Bot telah dimulai! Tutup aplikasi Telegram dan bot akan menghitung mundur 3 jam.')

def stop_timer():
    global countdown_timer
    if countdown_timer:
        countdown_timer.cancel()
        countdown_timer = None

async def notify_user(bot: Bot, chat_id: int):
    await bot.send_message(chat_id=chat_id, text='3 jam telah berlalu sejak Anda menutup aplikasi Telegram!')

async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global countdown_timer

    # Batalkan timer sebelumnya jika ada
    stop_timer()

    # Set timer baru
    countdown_timer = Timer(10800, notify_user, [context.bot, update.message.chat_id])
    countdown_timer.start()

    await update.message.reply_text('Timer 3 jam telah dimulai. Anda akan menerima notifikasi setelah 3 jam.')

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_timer", set_timer))

    application.run_polling()

if __name__ == '__main__':
    main()
