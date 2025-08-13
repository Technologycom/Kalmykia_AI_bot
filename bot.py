import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from mistralai import Mistral
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем ключи из .env
api_key = os.getenv("MISTRAL_API_KEY")
bot_token = os.getenv("BOT_TOKEN")
model = "mistral-small-latest"

# Проверка, что ключи указаны
if not api_key or not bot_token:
    raise ValueError("Проверьте, что в файле .env указаны MISTRAL_API_KEY и BOT_TOKEN")

# Инициализация клиента Mistral
client = Mistral(api_key=api_key)

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=bot_token)
dp = Dispatcher()

# /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я ИИ-бот, Микаса. Напиши или спроси у меня что-нибудь, и я отвечу 🙂")

# Ответ на все сообщения
@dp.message()
async def handle_message(message: types.Message):
    response = client.chat.complete(
        model=model,
        messages=[
            {"role": "user", "content": message.text},
        ]
    )
    await message.answer(response.choices[0].message.content)

# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
