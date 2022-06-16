from datetime import datetime, timedelta
from .tables import Channel, Post, Complain, Blacklist
from .messageClass import ChannelMessage

class ComplainAction(ChannelMessage):
    '''
    Класс для работы с жалобами в БД
    '''
    def __init__(self, message, author):
        super().__init__(message)
        self.author = author
        self.get_channel = self.s.query(Channel).where(Channel.id_telegram == self.chat_id).one_or_none()
        self.get_complain = self.s.query(Complain).filter((Complain.channel_id == self.chat_id)
                                                    & (Complain.author_id == author)
                                                    & (Complain.post_id == self.message_id)).\
                                                    one_or_none()

    def save_complain(self):
        '''
        Сохраняет жалобу в БД, если от пользователя она не поступала на данный пост
        '''

        if not self.get_complain:
            new_complain = Complain(post_id = self.message_id, author_id = self.author,
                                    channel_id = self.chat_id, created_at = datetime.now(),
                                    updated_at = datetime.now())
            self.s.add(new_complain)
            self.s.commit()
            return 'Жалоба отправлена!'
        else:
            return 'Вы уже жаловались на этот пост!'

    def delete_complain(self):
        '''
        Удаляем жалобу от пользователя в БД, если она существует
        '''

        if self.get_complain:
            self.s.delete(self.get_complain)
            self.s.commit()

    def count_of_complains(self):
        '''
        Возвращает количество жалоб на пост
        '''
    
        #Сохраняем количество голосов для блокировки
        votes_for_block = self.get_channel.votes_for_block

        if self.get_complain:
            post_id = self.get_complain.post_id
            channel_id = self.get_complain.channel_id

            complains_count = self.s.query(Complain).filter((Complain.post_id == post_id)
                                                & (Complain.channel_id == channel_id)).\
                                                count()
            
            return {'count': complains_count, 'count_for_block': votes_for_block}

    def block_author(self):
        '''
        Временно или навсегда блокирует автора постов
        '''

        #Сохраняем длительность блокировки на канале
        mute_timer = self.get_channel.mute_timer

        #Запрашиваем в БД пост
        get_post = self.s.query(Post).filter((Post.channel_id == self.chat_id) & (Post.id_telegram == self.message_id)).one()

        #Сохраняем id автора поста в переменную
        post_author = get_post.author_id

        #Проверяем, что пользователь ранее не блокировался
        check_ban = self.s.query(Blacklist).filter((Blacklist.id_telegram == post_author) & (Blacklist.channel_id == self.chat_id)).one_or_none()

        #Блокируем автора на время, если ранее не блокировался, баним, если ранее блокировался
        if not check_ban:
            mute_end_date = datetime.now() + timedelta(days=mute_timer)
            mute_author = Blacklist(id_telegram = post_author, channel_id = self.chat_id,
                                    type_of_access_restriction = 'mute', mute_end_date = mute_end_date,
                                    created_at = datetime.now(), updated_at = datetime.now())
            self.s.add(mute_author)
            self.s.commit()

            #Переводим дату разблокировки в Московское время
            mute_end_date = mute_end_date + timedelta(hours=3)
            mute_end_date = mute_end_date.isoformat('T', 'minutes')
            
            return f'заблокирован до {mute_end_date} по МСК. При повторном инциденте автор будет заблокирован навсегда.'
        else:
            check_ban.type_of_access_restriction = 'ban'
            check_ban.updated_at = datetime.now()
            self.s.add(check_ban)
            self.s.commit()

            return 'заблокирован навсегда.'