import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7641349601:AAFZ2ZabpcEBTFVNcd4Dz3Wtu76q6Lbzrj4"

# Simple memory storage of user limits (for MVP)
user_limits = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, красотка! Я твой личный ПП-тренер. Отправь фото еды — я скажу, сколько там калорий 🍒")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_limits.setdefault(user_id, 0)
    if user_limits[user_id] >= 3:
        await update.message.reply_text("Ты использовала дневной лимит 💔 Хочешь безлимит? Оформи подписку за 299 ₽.")
        return

    user_limits[user_id] += 1
    await update.message.reply_text("Фото получено! Я анализирую... 🍽 (тут будет калорийность)")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()
