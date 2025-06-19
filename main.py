import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import aiohttp
import base64

openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь фото еды — я скажу, сколько там калорий 🍽️")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    photo_bytes = await file.download_as_bytearray()
    photo_b64 = base64.b64encode(photo_bytes).decode()

    await update.message.reply_text("Фото получено! Анализирую через GPT-4o Vision...")

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "Ты помощник, который определяет продукты питания на фото и оценивает калорийность."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Что на этом фото? Примерно сколько калорий?"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{photo_b64}"}}
                    ]
                }
            ],
            max_tokens=300,
        )

        result = response.choices[0].message.content
        await update.message.reply_text(result)
    except Exception as e:
        logging.error(f"Ошибка Vision: {e}")
        await update.message.reply_text("Ошибка при анализе фото 😔")

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()
