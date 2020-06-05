import logging

from symbot.chat.message import Message
from symbot.dynamic.commands._base_command import BaseCommand
from symbot.control.control import Control


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!int'
        self.author = 'fd_symbicort'
        self.cooldown = 20

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
        logging.info(f'({self.name}) successfully generated response')
