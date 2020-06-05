import logging

from symbot.chat.message import Message
from symbot.control.control import Control
from symbot.dev.commands._base_command import BaseCommand


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!deaths'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):

        try:
            broadcaster = self.control.environment.get('broadcaster')
        except KeyError:
            logging.info(f'{self.name} unable to find var broadcaster')
            return
        try:
            deaths = self.control.environment.get('deaths')
        except KeyError:
            logging.info(f'{self.name} unable to find var deaths')
            return

        response = f'{broadcaster} has died {deaths} times :('
        await self.control.respond(response)
