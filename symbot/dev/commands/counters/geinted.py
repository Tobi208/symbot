from symbot.chat.message import Message
from symbot.control.control import Control
from symbot.dev.commands._base_command import BaseCommand


class Command(BaseCommand):

    def __init__(self, control: Control):
        super().__init__(control)
        self.name = '!geinted'
        self.author = 'fd_symbicort'

    async def run(self, msg: Message):

        msg.command = '!int'

        await self.control.requeue(msg)
