from aiogram import executor
from create_bot import dp
from src.handlers import admin, posting

#Администрирование
admin.register_handlers_admin(dp)

#Посты
posting.register_handlers_posting(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)