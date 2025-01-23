import aiohttp
import asyncio
import os
from gtts import gTTS
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from googletrans import Translator
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
async def main():
    dp.message.register(weather_command, Command(commands=["weather"]))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# # Переводчик
# translator = Translator()
# # Флаг для отслеживания режима перевода
# user_translation_mode = {}
#
# # Команда /translation
# @dp.message(Command("translation"))
# async def start_translation(message: Message):
#     user_translation_mode[message.from_user.id] = True
#     await message.answer("Напишите текст, который вы хотите перевести на английский.\nЧтобы выйти из режима перевода, отправьте команду /stop_translation.")
#
# # Остановка перевода
# @dp.message(Command("stop_translation"))
# async def stop_translation(message: Message):
#     user_translation_mode[message.from_user.id] = False
#     await message.answer("Режим перевода отключен.")
#
# # Обработка текста для перевода
# @dp.message()
# async def handle_text(message: Message):
#     # Проверяем, включен ли режим перевода для пользователя
#     if user_translation_mode.get(message.from_user.id):
#         try:
#             # Перевод текста на английский
#             translation = translator.translate(message.text, dest="en")
#             translated_text = translation.text
#             await message.answer(f"Перевод на английский:\n{translated_text}")
#         except Exception as e:
#             await message.answer(f"Произошла ошибка при переводе: {e}")
@dp.message(Command('training'))
async def training(message: Message):
   training_list = [
       "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

   tts = gTTS(text=rand_tr, lang='ru')
   tts.save("training.ogg")
   audio = FSInputFile('training.ogg')
   await bot.send_voice(message.chat.id, voice=audio)
   os.remove("training.ogg")
@dp.message(Command('video'))
async def video(message: Message):
    video = FSInputFile('img/video.mp4')
    await bot.send_video(message.chat.id, video)
    await bot.send_chat_action(message.chat.id, 'upload_video')
@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile('img/voice.ogg')
    await message.answer_voice(voice)
@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile('img/Презентация КЛ.pdf')
    await message.answer_document(doc)
@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('img/audio.mp3')
    await bot.send_audio(message.chat.id, audio)

IMG_FOLDER = "img"
if not os.path.exists(IMG_FOLDER):
    os.makedirs(IMG_FOLDER)
@dp.message(Command("photo"))
async def send_random_photo(message: Message):
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
@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\\n/start\\n/help\\n/photo\\n/video\\n/audio\\n/minitraining\\n/weather")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}")
@dp.message()
async def start(message: Message):
    if message.text.lower() == 'test':
        await message.answer('Тестируем')
@dp.message()
async def start(message: Message):
    await message.answer("Я тебе ответил")

# Переводчик
translator = Translator()
# Флаг для отслеживания режима перевода
user_translation_mode = {}

# Команда /translation
@dp.message(Command("translation"))
async def start_translation(message: Message):
    user_translation_mode[message.from_user.id] = True
    await message.answer("Напишите текст, который вы хотите перевести на английский.\nЧтобы выйти из режима перевода, отправьте команду /stop_translation.")

# Остановка перевода
@dp.message(Command("stop_translation"))
async def stop_translation(message: Message):
    user_translation_mode[message.from_user.id] = False
    await message.answer("Режим перевода отключен.")

# Обработка текста для перевода
@dp.message()
async def handle_text(message: Message):
    # Проверяем, включен ли режим перевода для пользователя
    if user_translation_mode.get(message.from_user.id):
        try:
            # Перевод текста на английский
            translation = translator.translate(message.text, dest="en")
            translated_text = translation.text
            await message.answer(f"Перевод на английский:\n{translated_text}")
        except Exception as e:
            await message.answer(f"Произошла ошибка при переводе: {e}")

# # Функция для получения прогноза погоды
# async def get_weather(city: str) -> str:
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url) as response:
#                 if response.status != 200:
#                     return "Ошибка: Не удалось получить данные о погоде. Проверьте название города."
#                 data = await response.json()
#
#                 if data.get("cod") != 200:
#                     return f"Ошибка: {data.get('message', 'Не удалось получить данные о погоде')}"
#
#                 city_name = data["name"]
#                 temp = data["main"]["temp"]
#                 description = data["weather"][0]["description"].capitalize()
#
#                 return f"Погода в {city_name}: {description}, температура: {temp}°C"
#     except aiohttp.ClientError:
#         return "Не удалось получить данные о погоде. Проверьте соединение с интернетом."
#
# # Команда /weather
# async def weather_command(message: Message):
#     args = message.text.split(maxsplit=1)
#     if len(args) > 1:
#         city = args[1]
#         forecast = await get_weather(city)
#         await message.reply(forecast)
#     else:
#         await message.reply("Пожалуйста, укажите город. Например: /weather Москва")
#
# async def main():
#     dp.message.register(weather_command, Command(commands=["weather"]))
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

