import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dadata import Dadata
import random
import requests
from googletrans import Translator
from datetime import datetime, timedelta
from config import TOKEN, DADATA_TOKEN, DADATA_SECRET

# Инициализация бота и Dadata
bot = Bot(token=TOKEN)
dp = Dispatcher()
dadata = Dadata(DADATA_TOKEN, DADATA_SECRET)

# Логирование
logging.basicConfig(level=logging.INFO)

@dp.message(Command("start", "help"))
async def send_welcome(message: Message):
    await message.reply("Привет! Отправьте мне адрес, и я его стандартизирую через DaData.")

@dp.message()
async def clean_address(message: Message):
    try:
        address = message.text
        result = dadata.clean("address", address)
        if result:
            formatted_address = result.get("result", "Не удалось стандартизировать адрес.")
        else:
            formatted_address = "Ошибка обработки."
        await message.reply(f"Стандартизированный адрес: {formatted_address}")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.reply("Произошла ошибка при обработке запроса.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



# async def main():
#    await dp.start_polling(bot)
#
# if __name__ == '__main__':
#    asyncio.run(main())