import re
import time
from symbot.config import prefix


class Message:
    """Represents a message received from Twitch as workable object"""

    def __init__(self, received):
        """
        Parameters
        ----------
         received : str
            private message from Twitch channel
        """

        # parser that works on private messages from twitch channel
        # maybe try/catch for correct input just in case
        # maybe expand to generic messages
        groups = re.search(':(.*)!.*@.*\.tmi\.twitch\.tv PRIVMSG (#.*)?:(.*)', received).groups()

        # user who sent message
        self.user = groups[0]
        # channel message was sent in
        self.channel = groups[1]
        # time since epoch
        self.timestamp = time.time()
        # content user intended to be received
        self.content = groups[2]
        # checks if message calls a command
        # maybe make it work without prefix
        #       as in: no prefix -> every message treated as command
        #       filter for existing commands in control unit
        self.is_command = self.content.startswith(prefix)
