from symbot import config
from symbot.chat.message import Message
from symbot.control.commands._base_command import BaseCommand
from symbot.control.control import Control


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!int'
        self.author = 'fd_symbicort'
        self.cooldown = 20

    async def run(self, msg: Message):
        bad = self.control.environment.increment('bad')
        response = f'{config.channel} hat schon {bad} mal den turbo int rausgehauen'
        await self.control.respond(response)
