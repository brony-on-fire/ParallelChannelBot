from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter
from time import time
from src.bases.db_operations import ChatPosting, ChannelPosting, ComplainAction
from src.markups.markups import mainMenu, comments_button
from create_bot import dp, bot

async def posting(message:types.Message):
    '''
    Создаёт пост в привязанном канале
    '''
    message_for_post = message.get_args()

    if not message_for_post:
        await message.reply('Вы не указали текст для поста.')
    else:
        new_post = ChatPosting(message)
        check_permission = new_post.check_permission_for_posting()
        if check_permission['status'] == False:
            message_for_answer = check_permission['message']
            await message.reply(message_for_answer)
        else:
            channel = check_permission['message']
            save_post = await bot.send_message(channel, message_for_post)

            #Сохраняем пост в БД
            save_post = ChannelPosting(save_post)
            save_post.save_post(author = message.from_user.id)

async def create_comment_button(message:types.Message):
    '''
    Создаёт кнопку со ссылкой на обсуждение в сообщении канала
    '''
    if message.is_automatic_forward:
        #Получаем информацию о посте
        channel_id = message.sender_chat.id
        post_id = message.forward_from_message_id

        #Формируем кнопку обсуждения
        message_id_for_url = message.message_id
        chat_id_for_url = str(message.chat.id)[4:]
        
        comments_button.url = f'https://t.me/c/{chat_id_for_url}/{message_id_for_url}?thread={message_id_for_url}'

        #Добавляем к посту клавиатуру
        await bot.edit_message_reply_markup(chat_id=channel_id, message_id=post_id, reply_markup=mainMenu)

async def complain(call:types.CallbackQuery):
    '''
    Обрабатывает нажатие на кнопку жалобы
    '''
    author = call.from_user.id

    #Сохраняем жалобу в БД
    new_complain = ComplainAction(call.message, author)
    save_complain_message = new_complain.save_complain()

    #Запрашиваем общее количество жалоб на пост
    count_of_complain = ComplainAction(call.message, author).count_of_complains()
    
    #После учета жалобы проверяем их общее количество и, при необходимости, блокируем пользователя
    if count_of_complain['count'] == count_of_complain['count_for_block']:
        block_author_message = new_complain.block_author()
        await call.message.edit_text(text = f'Пост удален за многочисленные жалобы. Автор поста {block_author_message}')
    else:
        #Отправляем сообщение, что жалоба обработана
        await call.answer(text = f'{save_complain_message}', cache_time=10)

def register_handlers_posting(dp:Dispatcher):
    dp.register_message_handler(posting, ChatTypeFilter(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP]), commands=['post'])
    dp.register_message_handler(create_comment_button, ChatTypeFilter(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP]), content_types=['text'])
    dp.register_callback_query_handler(complain, text_contains='complain')