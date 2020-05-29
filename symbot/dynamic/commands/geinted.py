from symbot.chat.message import Message
from symbot.dynamic.commands._base_command import BaseCommand
from symbot.control.control import Control


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!geinted'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):
        msg.command = 'int'
        await self.control.requeue(msg)
