from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter
from src.bases.db_operations import ChannelMessage
from create_bot import dp

async def link_chat(message: types.Message):
    '''
    Связывает канал с чатом
    '''
    linked_chat_id = message.text[10:]

    if linked_chat_id == '':
        await message.reply('Вы не указали id чата для связывания.')
    else:
        new_link = ChannelMessage(message)
        new_link.connect_chat(linked_chat_id)
        await message.reply('Привязка осуществлена.')

async def get_id(message: types.Message):
    '''
    Возвращает id чата
    '''
    await message.reply(message.chat.id)

def register_handlers_admin(dp:Dispatcher):
    dp.register_channel_post_handler(link_chat, text_startswith=['link_chat '])
    dp.register_message_handler(get_id, ChatTypeFilter(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP]), commands=['get_id'])