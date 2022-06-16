from datetime import datetime
from .tables import Post
from .messageClass import ChannelMessage

class ChannelPosting(ChannelMessage):
    '''
    Класс для действий с постами в БД
    '''
    def save_post(self, author):
        '''
        Сохраняет информацию о добавленом посте
        '''

        new_post = Post(id_telegram = self.message_id, channel_id = self.chat_id,
                        author_id = author, created_at = datetime.now(),
                        updated_at = datetime.now())
        self.s.add(new_post)
        self.s.commit()