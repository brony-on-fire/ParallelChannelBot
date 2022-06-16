from datetime import datetime
from .tables import Channel
from .messageClass import ChannelMessage

class ChannelSetting(ChannelMessage):
    '''
    Класс для настроек канала
    '''
    def __init__(self, message):
        super().__init__(message)
        self.get_channel = self.s.query(Channel).where(Channel.id_telegram == self.chat_id).one_or_none()
        
    def connect_chat(self, linked_chat_id):
        '''
        Добавляет/изменяет связь канала и чата
        '''

        if self.get_channel is None:
            new_channel = Channel(id_telegram = self.chat_id, linked_chat_id = linked_chat_id,
                                mute_timer = 3, votes_for_block = 10,
                                created_at = datetime.now(), updated_at = datetime.now())
            self.s.add(new_channel)
            self.s.commit()
        else:
            self.get_channel.linked_chat_id = linked_chat_id
            self.get_channel.updated_at = datetime.now()
            self.s.add(self.get_channel)
            self.s.commit()

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
        self.s.commit()
        
        param_for_message = settings_dict[setting]
        
        return f"Параметр {param_for_message} обновлен!"