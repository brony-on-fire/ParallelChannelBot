from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter
from src.bases.ChannelSetting import ChannelSetting
from create_bot import dp

async def get_id(message: types.Message):
    '''
    Возвращает id чата
    '''
    await message.reply(message.chat.id)

async def link_chat(message: types.Message):
    '''
    Связывает канал с чатом
    '''
    linked_chat_id = message.text[10:]

    if linked_chat_id == '':
        await message.reply('Вы не указали id чата для связывания.')
    else:
        new_link = ChannelSetting(message)
        new_link.connect_chat(linked_chat_id)
        await message.reply('Привязка осуществлена.')

def register_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(get_id, ChatTypeFilter(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP]), commands=['get_id'])
    dp.register_channel_post_handler(link_chat, text_startswith=['link_chat '])