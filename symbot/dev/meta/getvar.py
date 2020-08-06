import logging

from symbot.chat.message import Message
from symbot.dev.meta._base_meta_command import BaseMetaCommand


class Command(BaseMetaCommand):

    def __init__(self, control):
        super().__init__(control)
        self.name = '!getvar'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):

        try:
            var = msg.context[0]
        except IndexError:
            logging.info(f'{self.name} missing context var')
            return
        try:
            val = self.control.environment.get(var)
        except KeyError:
            logging.info(f'{self.name} unable to find var {var}')
            return

        response = f'{var} has value {val}'
        await self.control.respond(response)
