from datetime import datetime, timedelta
from .tables import Channel, Blacklist
from .messageClass import ChatMessage

class ChatPosting(ChatMessage):
    '''
    Класс для действий с БД при отправке сообщений в канал
    '''   
    def check_permission_for_posting(self):
        '''
        Проверяет, что можно постить в канал
        '''
        #Проверяем, что у чата установлена связь с каким-либо каналом
        get_channel = self.s.query(Channel).where(Channel.linked_chat_id == self.chat_id).one_or_none()

        if get_channel is None:
            return {'status': False, 'message': 'Чат не привязан к какому-либо каналу!'}
        else:
            channel_id = get_channel.id_telegram

        #Проверяем, что пользователь не забанен
        check_ban = self.s.query(Blacklist).filter((Blacklist.id_telegram == self.user_id) & (Blacklist.channel_id == channel_id)).one_or_none()

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