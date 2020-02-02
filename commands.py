import time

from messages import Message


class Command(object):
    def __init__(self, message=None):
        self._message = message

    @property
    def message(self) -> Message:
        return self._message

    @message.setter
    def message(self, message: Message):
        self._message = message


class BarkCommand(Command):
    REACTS_TO = 'bark'

    def process(self) -> Message:
        self._message.reply = 'BARK!!BARK!!BARK!!'
        self._message.reply_generated_at = int(time.time())
        return self._message


class CommandFactory(object):
    REGISTERED_COMMANDS = Command.__subclasses__()

    @classmethod
    def build(cls, command: str, message: Message) -> Command:
        if command == 'bark':
            return BarkCommand(message)
        else:
            raise NameError('Unknown command')
