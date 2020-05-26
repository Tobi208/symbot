from abc import ABC, abstractmethod

from symbot.chat.message import Message
from symbot.control.control import Control


class BaseCommand(ABC):
    """Abstract base class to implement new commands

    Abstract base class developers need to implement for new commands.
    Enforces all properties and methods required by controller.
    """

    @property
    @abstractmethod
    def control(self) -> Control:
        """central controller"""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """command identifier"""
        ...

    @property
    @abstractmethod
    def permission_level(self) -> int:
        """permission level of command"""
        ...

    @property
    @abstractmethod
    def cooldown(self) -> float:
        """minimum time between command calls"""
        ...

    @abstractmethod
    async def run(self, msg: Message):
        """execute command under consideration of user message

        Parameters
        ----------
        msg : Message
            message sent by user
        """
        ...
