import logging

from symbot.chat.message import Message
from symbot.control.control import Control
from symbot.dev.commands._base_command import BaseCommand


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!int'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):

        try:
            broadcaster = self.control.environment.get('broadcaster')
        except KeyError:
            logging.info(f'({self.name}) unable to find var (broadcaster)')
            return
        try:
            bad = self.control.environment.increment('bad')
        except KeyError:
            logging.info(f'({self.name}) unable to find var (bad)')
            return
        except TypeError:
            logging.info(f'({self.name}) unable to increment var (bad)')
            return

        response = f'{broadcaster} hat schon {bad} mal den turbo int rausgehauen'
        await self.control.respond(response)
