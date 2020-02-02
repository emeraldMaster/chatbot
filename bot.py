import argparse
import glob
import json
import os
import uuid

from messages import MessageFactory, Message
from commands import CommandFactory, BarkCommand

INBOUND_MESSAGES_DB = '{}/inbound'.format(os.getcwd())


class Dispatcher(object):
    SUPPORTED_COMMANDS = {cls.REACTS_TO: cls for cls in [BarkCommand]}

    def handle_command(self, command_name: str, param_json: str):
        if command_name == 'process':
            self._process_queue()
            return

        if command_name not in self.SUPPORTED_COMMANDS.keys():
            raise AttributeError('Unsupported command')

        if param_json and param_json != '':
            raw_message_data = json.loads(param_json)
            message = MessageFactory.build(raw_message_data)
        else:
            raise AttributeError('Message metadata is missing')
        self._add_to_queue(command_name, message)

    def _add_to_queue(self, command_name: str, message: Message):
        filename = '{}/{}.json'.format(INBOUND_MESSAGES_DB, uuid.uuid4())
        data = {'command_name': command_name, 'message': message.to_json()}
        with open(filename, 'w') as f:
            json.dump(data, f)
        print('new message added to the queue: {}'.format(filename))

    def _process_queue(self):
        for file in glob.glob('{}/*.json'.format(INBOUND_MESSAGES_DB)):
            with open(file, 'r') as f:
                raw_data = json.load(f)

            message = MessageFactory.build(raw_data['message'])
            command = CommandFactory.build(raw_data['command_name'], message)
            command.process()
            print(message.reply)
            os.remove(file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("ChatBot for Slack, Telegram or whatever")
    parser.add_argument('command', help='command for the bot')
    parser.add_argument('--json-meta', help='JSON for command')
    args = parser.parse_args()
    d = Dispatcher()
    d.handle_command(args.command, args.json_meta)

# "{\"source\": \"slack\", \"uid\": 123}"
