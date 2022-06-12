from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter
from src.bases.db_operations import ChatMessage, ChannelMessage
from src.markups.markups import mainMenu
from create_bot import dp, bot

async def posting(message:types.Message):
    '''
    Создаёт пост в привязанном канале
    '''
    message_for_post = message.get_args()

    if not message_for_post:
        await message.reply('Вы не указали текст для поста.')
    else:
        new_post = ChatMessage(message)
        check_permission = new_post.check_permission_for_posting()
        if check_permission['status'] == False:
            message_for_answer = check_permission['message']
            await message.reply(message_for_answer)
        else:
            channel = check_permission['message']
            save_post = await bot.send_message(channel, message_for_post, reply_markup=mainMenu)
            save_post = ChannelMessage(save_post)
            save_post.save_post(author = message.from_user.id)

async def complain(message:types.Message):
    await message.reply('Не нажимать!')

def register_handlers_posting(dp:Dispatcher):
    dp.register_message_handler(posting, ChatTypeFilter(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP]), commands=['channel_post'])
    dp.register_callback_query_handler(complain, text='complain')