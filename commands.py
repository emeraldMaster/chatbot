import time

from messages import Message


class CommandFactory(object):
    @classmethod
    def build(cls, command: str):
        if command == 'bark':
            return BarkCommand()
        else:
            raise NameError('Unknown command')


class BarkCommand(object):
    REACTS_TO = 'bark'

    def process(self, message: Message) -> Message:
        message.reply = 'BARK!!BARK!!BARK!!'
        message.reply_generated_at = int(time.time())
        return message
