import logging

from symbot.chat.message import Message
from symbot.dev.meta._base_meta_command import BaseMetaCommand


class Command(BaseMetaCommand):

    def __init__(self, control):
        super().__init__(control)
        self.name = '!setvar'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):

        try:
            var = msg.context[0]
        except IndexError:
            logging.info(f'{self.name} missing context var')
            return
        try:
            new_value = msg.context[1]
        except IndexError:
            logging.info(f'{self.name} missing context value')
            return
        self.control.environment.set(var, new_value)

        response = f'value of {var} has been changed to {new_value}'
        await self.control.respond(response)
