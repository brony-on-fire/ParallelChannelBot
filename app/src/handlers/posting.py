from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.utils.exceptions import BotKicked, Unauthorized
from aiogram.utils.markdown import escape_md
from time import time
from src.bases.ChatPosting import ChatPosting
from src.bases.ChannelPosting import ChannelPosting
from src.bases.ComplainAction import ComplainAction
from src.markups.markups import mainMenu, comments_button
from create_bot import dp, bot

async def posting(message:types.Message):
    '''
    Создаёт пост в привязанном канале
    '''
    author = message.from_user.id

    if message.reply_to_message:
        message_for_post = message.reply_to_message.text
    else:
        message_for_post = message.get_args()

    try:
        if not message_for_post:
            await message.reply('Вы не указали текст для поста.')
        elif message.reply_to_message and (author != message.reply_to_message.from_user.id):
            await message.reply('Вы можете переслать в канал только свое сообщение.')
        else:
            new_post = ChatPosting(message)

            #Проверяем, что пользователь может постить в канал
            check_permission = new_post.check_permission_for_posting()
            if check_permission['status'] == False:
                message_for_answer = check_permission['message']
                await message.reply(message_for_answer)
            else:
                channel = check_permission['message']

                #Отправляем пост в канал cо ссылкой на автора, если он подписан
                user_status = await bot.get_chat_member(channel, author)
                if isinstance(user_status, types.ChatMemberMember | types.ChatMemberOwner | types.ChatMemberAdministrator):
                    message_for_post = escape_md(message_for_post) + f'\n\n[Ссылка на автора](tg://user?id={author})'
                    save_post = await bot.send_message(channel, message_for_post,  parse_mode="MarkdownV2")
                else:
                    save_post = await bot.send_message(channel, message_for_post)

                #Сохраняем пост в БД
                save_post = ChannelPosting(save_post)
                save_post.save_post(author)
    except (BotKicked, Unauthorized):
        await message.reply('Бот больше не состоит в привязанном к чату канале.')

async def create_comment_button(message:types.Message):
    '''
    Создаёт кнопку со ссылкой на обсуждение в сообщении канала
    '''
    if message.is_automatic_forward:
        #Получаем информацию о посте
        channel_id = message.sender_chat.id
        post_id = message.forward_from_message_id

        #Проверяем, что пост есть в БД (то есть создан ботом, а не вручную)
        if ChannelPosting(message).post_exist(channel_id, post_id):

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
    save_complain_message = new_complain.save_delete_complain()

    #Запрашиваем общее количество жалоб на пост
    count_of_complain = ComplainAction(call.message, author).count_of_complains()
    
    #После учета жалобы проверяем их общее количество и, при необходимости, блокируем пользователя
    if count_of_complain['count'] >= count_of_complain['count_for_block']:
        block_author_message = new_complain.block_author()
        if block_author_message:
            await call.message.edit_text(text = f'Пост удален за многочисленные жалобы. Автор поста {block_author_message}')
        else:
            await call.answer(text = 'Автор поста уже был заблокирован за более поздний пост.', cache_time=1)
    else:
        #Отправляем сообщение, что жалоба обработана
        await call.answer(text = f'{save_complain_message}', cache_time=1)

def register_handlers_posting(dp:Dispatcher):
    dp.register_message_handler(posting, ChatTypeFilter(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP]), commands=['post'])
    dp.register_message_handler(create_comment_button, ChatTypeFilter(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP]), content_types=['text'])
    dp.register_callback_query_handler(complain, text_contains='complain')