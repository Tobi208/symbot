from symbot import config
from symbot.chat.message import Message
from symbot.control.commands._base_command import BaseCommand
from symbot.control.control import Control


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!deaths'
        self.author = 'fd_symbicort'
        self.permission_level = 3
        self.cooldown = 5

    async def run(self, msg: Message):
        deaths = self.control.environment.get('deaths')
        response = f'{config.channel} has died {deaths} times :('
        await self.control.respond(response)
