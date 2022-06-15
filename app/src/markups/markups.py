from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#Клавиатура для добавления жалобы
mainMenu = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
complain = InlineKeyboardButton(text='Жалоба ⚠️', callback_data='complain')
comments_button = InlineKeyboardButton(text='Обсуждение 💬', url = 'https://telegram.org/')

mainMenu.insert(complain)
mainMenu.insert(comments_button)