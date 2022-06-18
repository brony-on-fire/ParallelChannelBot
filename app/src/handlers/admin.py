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

async def mute_timer(message: types.Message):
    '''
    Задает количество дней для блока
    '''
    mute_timer_value = message.text[11:]

    if mute_timer_value == '':
        await message.reply('Вы не указали количество дней блокировки.')
    else:
        update_timer = ChannelSetting(message).set_setting("mute_timer", mute_timer_value)
        await message.reply(f'{update_timer}')

async def vote_for_block(message: types.Message):
    '''
    Задает количество жалоб для блока
    '''
    vote_value = message.text[15:]

    if vote_value == '':
        await message.reply('Вы не указали количество жалоб для блокировки.')
    else:
        update_vote = ChannelSetting(message).set_setting("votes_for_block", vote_value)
        await message.reply(f'{update_vote}')

def register_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(get_id, ChatTypeFilter(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP]), commands=['get_id'])
    dp.register_channel_post_handler(link_chat, ChatTypeFilter(chat_type=[types.ChatType.CHANNEL]), text_startswith=['link_chat '])
    dp.register_channel_post_handler(mute_timer, ChatTypeFilter(chat_type=[types.ChatType.CHANNEL]), text_startswith=['mute_timer '])
    dp.register_channel_post_handler(vote_for_block, ChatTypeFilter(chat_type=[types.ChatType.CHANNEL]), text_startswith=['vote_for_block '])