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

    def post_exist(self, channel_id, post_id):
        '''
        Проверяет, что пост существует
        '''

        #Запрашиваем в БД пост
        get_post = self.s.query(Post).filter((Post.channel_id == channel_id) & (Post.id_telegram == post_id)).one_or_none()

        if get_post:
            return True
        else:
            return False