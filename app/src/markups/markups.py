from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

mainMenu = InlineKeyboardMarkup(row_width=1)
complain = InlineKeyboardButton(text='Пожаловаться ⚠️', callback_data='complain')

mainMenu.insert(complain)