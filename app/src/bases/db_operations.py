from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .tables import engine_settings, Base, Channel, Post, Vote, Blacklist

engine = create_engine(engine_settings)
session = sessionmaker(bind=engine)
s = session()

class ChatMessage:
    '''
    Класс для работы с сообщениями в чате
    '''
    def __init__(self, message):
        self.message_id = message.message_id
        self.chat_id = message.chat.id
        self.user_id = message.from_user.id
        self.user_name = message.from_user.username
        self.first_name = message.from_user.first_name
        self.last_name = message.from_user.last_name
    
    def check_permission_for_posting(self):
        '''
        Проверяет, что можно постить в канал
        '''
        #Проверяем, что у чата установлена связь с каким-либо каналом
        get_channel = s.query(Channel).where(Channel.linked_chat_id == self.chat_id).one_or_none()

        if get_channel is None:
            return {'status': False, 'message': 'Чат не привязан к какому-либо каналу!'}
        else:
            channel_id = get_channel.id_telegram

        #Проверяем, что пользователь не забанен
        check_ban = s.query(Blacklist).where(Blacklist.id_telegram == self.user_id and Blacklist.channel_id == channel_id).one_or_none()

        if check_ban is not None:
            check_ban_status = check_ban.type_of_access_restriction
            mute_end_date = check_ban.mute_end_date
            if check_ban_status == 'ban':
                return {'status': False, 'message': 'Вы заблокированы за многочисленные жалобы. Больше Вы не можете постить в канал. Функционала по разблокировке еще нет, поэтому страдайте вечно.'}  
            elif check_ban_status == 'mute' and  mute_end_date > datetime.now():
                mute_end_date = mute_end_date + timedelta(hours=3)
                mute_end_date = mute_end_date.isoformat('T', 'minutes')
                return {'status': False, 'message': f'Вы не можете постить в канал за многочисленные жалобы до {mute_end_date} по МСК'}

        return {'status': True, 'message': channel_id}

class ChannelMessage:
    '''
    Класс для работы с постами в канале
    '''
    def __init__(self, message):
        self.message_id = message.message_id
        self.chat_id = message.chat.id
        self.get_channel = s.query(Channel).where(Channel.id_telegram == self.chat_id).one_or_none()

    def connect_chat(self, linked_chat_id):
        '''
        Добавляет/изменяет связь канала и чата
        '''

        if self.get_channel is None:
            new_channel = Channel(id_telegram = self.chat_id, linked_chat_id = linked_chat_id,
                                mute_timer = 3, votes_for_block = 10,
                                created_at = datetime.now(), updated_at = datetime.now())
            s.add(new_channel)
            s.commit()
        else:
            self.get_channel.linked_chat_id = linked_chat_id
            self.get_channel.updated_at = datetime.now()
            s.add(self.get_channel)
            s.commit()

    def set_setting(self, setting, value):
        '''
        Изменяет настройки чата
        '''

        settings_dict = {"mute_timer": "'Таймер блокировки'", "votes_for_block": "'Количество жалоб для блокировки'"}

        #Проверяем, что канал привязан к чату   
        if self.get_channel is None:
            return 'Канал еще ни разу не привязывался к чату - нечего настраивать.'
        
        #Проверяем, что пользователь указал параметр в правильном формате
        try:
            value = int(value)
        except ValueError:
            return "Неправильный формат числа!"
        
        match setting:
            case "mute_timer":
                self.get_channel.update({Channel.mute_timer: value, Channel.updated_at: datetime.now()})
            case "votes_for_block":
                self.get_votes_for_block.update({Channel.votes_for_block: value, Channel.updated_at: datetime.now()})
        s.commit()
        
        param_for_message = settings_dict[setting]
        
        return f"Параметр {param_for_message} обновлен!"

    def save_post(self, author):
        '''
        Сохраняет информацию о добавленом посте
        '''

        new_post = Post(id_telegram = self.message_id, channel_id = self.chat_id,
                        author_id = author, created_at = datetime.now(),
                        updated_at = datetime.now())
        s.add(new_post)
        s.commit()