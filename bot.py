import argparse
import json
import time

from messages import MessageFactory
from commands import CommandFactory, BarkCommand

INBOUND_MESSAGES_DB = "inbound.jsonl"
OUTBOUND_MESSAGEWS_DB = "outbound.jsonl"


class Dispatcher(object):
    SUPPORTED_COMMANDS = {cls.REACTS_TO: cls for cls in [BarkCommand]}

    def handle_command(self, command_name: str, param_json: str):
        if command_name not in self.SUPPORTED_COMMANDS.keys():
            raise AttributeError('Unsupported command')

        command = CommandFactory.build(command_name)

        if param_json and param_json != '':
            raw_message_data = json.loads(param_json)
            message = MessageFactory.build(raw_message_data)
        else:
            raise AttributeError('Message metadata is missing')
        command.process(message)
        print(message.reply)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("ChatBot for Slack, Telegram or whatever")
    parser.add_argument('command', help='command for the bot')
    parser.add_argument('params', help='params for command')
    args = parser.parse_args()
    d = Dispatcher()
    d.handle_command(args.command, args.params)

# "{\"source\": \"slack\", \"uid\": 123}"
