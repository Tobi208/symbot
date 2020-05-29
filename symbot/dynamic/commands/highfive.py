from symbot.chat.message import Message
from symbot.dynamic.commands._base_command import BaseCommand
from symbot.control.control import Control


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!highfive'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):
        response = msg.user + ' hat ' + msg.context[0] + ' ein highfive gegeben'
        await self.control.respond(response)