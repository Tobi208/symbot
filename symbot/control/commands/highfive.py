import asyncio

from symbot.chat.message import Message
from symbot.control.commands._base_command import BaseCommand
from symbot.control.control import Control


class Command(BaseCommand):

    def __init__(self, control):
        super().__init__(control)
        self._name = 'highfive'
        self.author = 'fd_symbicort'
        self._permission_level = 3
        self._cooldown = 10

    async def run(self, msg: Message):
        response = msg.user + ' hat ' + msg.context[0] + ' ein highfive gegeben'
        await self.control.respond(response)
