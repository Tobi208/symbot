import asyncio

from symbot.chat.message import Message
from symbot.control.commands._base_command import BaseCommand
from symbot.control.control import Control


class Command(BaseCommand):

    def __init__(self, control):
        self._control = control
        self._name = 'highfive'
        self.author = 'fd_symbicort'
        self._permission_level = 3
        self._cooldown = 10

    @property
    def control(self) -> Control:
        return self._control

    @control.setter
    def control(self, value):
        self._control = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def permission_level(self) -> int:
        return self._permission_level

    @permission_level.setter
    def permission_level(self, value):
        self._permission_level = value

    @property
    def cooldown(self) -> float:
        return self._cooldown

    @cooldown.setter
    def cooldown(self, value):
        self._cooldown = value

    async def run(self, msg: Message):
        response = msg.user + ' hat ' + msg.context.split(' ')[0] + ' ein highfive gegeben'
        await self.control.respond(response)