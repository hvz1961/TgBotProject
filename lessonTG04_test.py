import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
import random

from gtts import gTTS
import os

from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.callback_query(F.data == 'news')
async def news(callback: CallbackQuery):
    await callback.answer("Новости подгружаются", show_alert=True)
    await callback.message.answer('Вот свежие новости!', reply_markup=await kb.test_keyboard())


@dp.message(F.text == "Тестовая кнопка 1")
async def test_button(message: Message):
    await message.answer('Обработка нажатия на reply кнопку')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer(
        "Этот бот умеет выполнять команды:\\n/start\\n/help\\n/photo\\n/video\\n/audio\\n/minitraining\\n/weather")


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}", reply_markup=kb.main)
    await message.answer(f"Привет, {message.from_user.full_name}", reply_markup=kb.inline_keyboard_test)
    # await message.answer(f"Привет, {message.from_user.full_name}", reply_markup=await kb.test_keyboard())


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

