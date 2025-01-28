import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
from gtts import gTTS
import os
from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    await message.answer('Динамика', reply_markup=kb.inline_keyboard_dynamic)

@dp.message(Command('links'))
async def links(message: Message):
    await message.answer('Ссылки', reply_markup=kb.inline_keyboard_links)

@dp.message(F.text == "Пока")
async def test_button(message: Message):
    await message.answer(f"До свидания, {message.from_user.full_name}")

@dp.message(F.text == "Привет")
async def test_button(message: Message):
    await message.answer(f"Здравствуй, {message.from_user.full_name}")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Старт", reply_markup=kb.main)

@dp.callback_query(F.data == "show_more")
async def show_more(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=kb.new_keyboard)

# Обработчик для кнопки "Опция 1"
@dp.callback_query(F.data == "option_1")
async def option_1(callback: CallbackQuery):
    # await callback.message.answer("Вы выбрали Опцию 1")
    await callback.message.answer("Вы выбрали Опцию 1", reply_markup=kb.back_keyboard)

# Обработчик для кнопки "Опция 2"
@dp.callback_query(F.data == "option_2")
async def option_2(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали Опцию 2", reply_markup=kb.back_keyboard)
    # await callback.message.answer("Вы выбрали Опцию 2")

# Обработчик для кнопки "Назад"
@dp.callback_query(F.data == "back_to_options")
async def back_to_options(callback: CallbackQuery):
    await callback.message.edit_text("Выберите опцию:", reply_markup=kb.options_keyboard)
async def main():
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())


