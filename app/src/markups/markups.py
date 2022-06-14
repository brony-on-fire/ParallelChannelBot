from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#Клавиатура для добавления жалобы
newComplain = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
complain = InlineKeyboardButton(text='Жалоба ⚠️', callback_data='complain')
comments = InlineKeyboardButton(text='Обсуждение 💬', callback_data='go_to_comments')

newComplain.insert(complain)
newComplain.insert(comments)