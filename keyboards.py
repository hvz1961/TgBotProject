from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
], resize_keyboard=True)

inline_keyboard_links = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Новости", url='https://ria.ru/20250128/ukraina-1995833499.html')],
   [InlineKeyboardButton(text="Музыка", url='https://www.premiumbeat.com/ru/royalty-free-tracks/rise-of-liberty')],
   [InlineKeyboardButton(text="Видео", url='https://youtube.com/shorts/JV0e33az6GE')],
])

inline_keyboard_dynamic = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Показать больше", callback_data="show_more")],
])

# Создаем новые кнопки
option1_button = InlineKeyboardButton(text="Опция 1", callback_data="option_1")
option2_button = InlineKeyboardButton(text="Опция 2", callback_data="option_2")

# Создаем новую клавиатуру с этими кнопками
new_keyboard = InlineKeyboardMarkup(inline_keyboard=[[option1_button, option2_button]])

# Создаем кнопку "Назад"
back_button = InlineKeyboardButton(text="Назад", callback_data="back_to_options")

# Создаем клавиатуру с кнопкой "Назад"
back_keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])

# Создаем клавиатуру с кнопками "Опция 1" и "Опция 2"
options_keyboard = InlineKeyboardMarkup(inline_keyboard=[[option1_button, option2_button]])


#
# test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]
#
# async def test_keyboard():
#    keyboard = InlineKeyboardBuilder()
#    for key in test:
#        keyboard.add(InlineKeyboardButton(text=key, url='https://youtube.com/shorts/JV0e33az6GE'))
#    return keyboard.adjust(2).as_markup()

# async def test_keyboard():
#    keyboard = ReplyKeyboardBuilder()
#    for key in test:
#        keyboard.add(KeyboardButton(text=key))
#    return keyboard.adjust(2).as_markup()