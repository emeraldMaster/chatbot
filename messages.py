import json
from enum import Enum
import time
from typing import Optional


class ChatPlatform(Enum):
    SLACK = 'slack'
    TELEGRAM = 'telegram'

    def __str__(self):
        return self.value


class MessageFactory(object):
    @classmethod
    def build(cls, raw_message_data: dict):
        platform = ChatPlatform(raw_message_data.get('source'))

        if platform == ChatPlatform.SLACK:
            return Message(source=platform, uid=raw_message_data['uid'],
                           text=raw_message_data.get('text'), created_at=None)


class Message(object):
    def __init__(self, source: ChatPlatform, uid: str, text: str, created_at: Optional[int] = None,
                 reply_generated_at: Optional[int] = None, reply: Optional[str] = None):
        self.source = source
        self.text = text
        self.uid = uid
        self.created_at = created_at if created_at else int(time.time())
        self.reply_generated_at = reply_generated_at
        self.reply = reply

    def to_json(self):
        attrs = self.__dict__
        attrs['source'] = str(attrs['source'])
        return attrs
