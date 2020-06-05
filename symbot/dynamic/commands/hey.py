import logging

from symbot.chat.message import Message
from symbot.control.control import Control
from symbot.dynamic.commands._base_command import BaseCommand


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = 'hey'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):
        response = f'Hey there, {msg.user} HeyGuys'
        await self.control.respond(response)
        logging.info(f'({self.name}) successfully generated response')
