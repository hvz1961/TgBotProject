import aiohttp
import asyncio
import os
from gtts import gTTS
from transliterate import translit
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from googletrans import Translator
from config import TOKEN, API_KEY
import random

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()
WEATHER_API_KEY = API_KEY

# Команда /start
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!\nЯ бот и могу помочь с:\n"
                         "/weather <город> - Узнать погоду\n"
                         "/photo - Получить фото\n"
                         "/translation - Перевод текста на английский\n"
                         "/help - Доступные команды")

# Команда /help
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Список доступных команд:\n"
                         "/start - Приветствие\n"
                         "/weather <город> - Узнать погоду\n"
                         "/photo - Получить фото\n"
                         "/translation - Перевод текста на английский"
                        )

# Команда /weather
async def get_weather(city: str) -> str:
    # Транслитерация города
    city_translit = translit(city, 'ru', reversed=True)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_translit}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return f"Ошибка: Город '{city}' не найден."
                data = await response.json()
                city_name = data.get("name", city)
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"].capitalize()
                return f"Погода в {city_name}: {description}, температура: {temp}°C"
    except Exception as e:
        return f"Ошибка: Не удалось получить данные о погоде. {e}"
@dp.message(Command("weather"))
async def weather_command(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        city = args[1]
        forecast = await get_weather(city)
        await message.answer(forecast)
    else:
        await message.answer("Пожалуйста, укажите город. Например: /weather Москва")
# Команда /translation
user_translation_mode = {}

@dp.message(Command("translation"))
async def start_translation(message: Message):
    user_translation_mode[message.from_user.id] = True
    await message.answer("Напишите текст для перевода на английский.\nОтправьте /stop_translation, чтобы выйти.")

@dp.message(Command("stop_translation"))
async def stop_translation(message: Message):
    user_translation_mode[message.from_user.id] = False
    await message.answer("Режим перевода отключен.")

IMG_FOLDER = "img"
if not os.path.exists(IMG_FOLDER):
    os.makedirs(IMG_FOLDER)
@dp.message(Command("photo"))
async def send_random_photo(message: Message):
    print("Команда /photo вызвана")
    images = [
        "https://avatarzo.ru/wp-content/uploads/podderjim-nashih.jpg",
        "https://avatarzo.ru/wp-content/uploads/orel.jpg",
        "https://avatarzo.ru/wp-content/uploads/volk-v-snegu.jpg",
    ]
    random_photo = random.choice(images)
    await message.answer_photo(photo=random_photo, caption="Это супер крутая картинка!")
# Обработчик для сохранения фотографий
@dp.message(F.photo)
async def save_user_photo(message: Message):
    responses = ["Ого, какая фотка!", "Непонятно, что это такое", "Не отправляй мне такое больше"]
    random_response = random.choice(responses)
    await message.answer(random_response)

    # Получаем фотографию с наивысшим разрешением
    photo = message.photo[-1]
    if photo and photo.file_id:  # Проверяем, что photo и file_id не None
        file_path = os.path.join(IMG_FOLDER, f"{photo.file_id}.jpg")
        try:
            # Скачиваем фото и сохраняем
            await bot.download(photo, destination=file_path)
            await message.answer("Фото успешно сохранено!")
        except Exception as e:
            await message.answer(f"Ошибка при сохранении фото: {e}")
    else:
        await message.answer("Не удалось обработать фото. Пожалуйста, попробуйте ещё раз.")
@dp.message(F.text & ~F.text.startswith('/'))
async def handle_text(message: Message):
    if user_translation_mode.get(message.from_user.id):
        translation = translator.translate(message.text, dest="en")
        await message.answer(f"Перевод:\n{translation.text}")

# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
