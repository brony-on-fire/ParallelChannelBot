from sqlalchemy.orm import sessionmaker
from .tables import engine

session = sessionmaker(bind=engine)

class ChatMessage:
    '''
    Класс для работы с сообщениями в чате
    '''
    def __init__(self, message):
        self.message_id = message.message_id
        self.chat_id = message.chat.id
        self.user_id = message.from_user.id
        self.s = session()

class ChannelMessage:
    '''
    Класс для работы с постами в канале
    '''
    def __init__(self, message):
        self.message_id = message.message_id
        self.chat_id = message.chat.id
        self.s = session()