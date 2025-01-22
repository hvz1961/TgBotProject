import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
# from aiogram.utils import executor
from config import TOKEN, API_KEY

import random

WEATHER_API_KEY = API_KEY
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения прогноза погоды
async def get_weather(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return "Ошибка: Не удалось получить данные о погоде. Проверьте название города."
                data = await response.json()

                if data.get("cod") != 200:
                    return f"Ошибка: {data.get('message', 'Не удалось получить данные о погоде')}"

                city_name = data["name"]
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"].capitalize()

                return f"Погода в {city_name}: {description}, температура: {temp}°C"
    except aiohttp.ClientError:
        return "Не удалось получить данные о погоде. Проверьте соединение с интернетом."

# Команда /weather
async def weather_command(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        city = args[1]
        forecast = await get_weather(city)
        await message.reply(forecast)
    else:
        await message.reply("Пожалуйста, укажите город. Например: /weather Москва")

@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://avatarzo.ru/wp-content/uploads/podderjim-nashih.jpg',
            'https://avatarzo.ru/wp-content/uploads/orel.jpg',
            'https://avatarzo.ru/wp-content/uploads/volk-v-snegu.jpg',
            ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')
@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\\n/start\\n/help\\n/photo\\n/weather")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")

async def main():
    dp.message.register(weather_command, Command(commands=["weather"]))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

