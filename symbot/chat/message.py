import re
import time
from symbot.config import prefix


class Message:
    """Represents a message received from Twitch as workable object

    Attributes
    ----------
    user : str
        user who sent the message
    channel : str
        channel message was sent to
    timestamp: float
        time since epoch
    content : str
        actual message sent by user
    is_command : bool
        flag if message was meant to call a command
    command : str
        name of command stripped of prefix
    """

    def __init__(self, received):
        """
        Parameters
        ----------
         received : str
            private message from Twitch channel
        """

        # regex parser that works on private messages from twitch channel
        # MAYBE try/catch for correct input just in case
        # MAYBE expand to generic messages
        groups = re.search(':(.*)!.*@.*\.tmi\.twitch\.tv PRIVMSG (#.*)?:(.*)', received).groups()

        self.user = groups[0]
        self.channel = groups[1]
        self.timestamp = time.time()
        self.content = groups[2]
        # MAYBE make it work without prefix
        #       as in: no prefix -> every message treated as commands
        #       filter for existing commands in control unit
        self.is_command = self.content.startswith(prefix)
        self.command = None
        # if message is meant to call a command
        # extract command from content
        if self.is_command:
            split = self.content.split(' ')
            self.command = split[0].strip(prefix)
            if split[1]:
                self.content = ' '.join(split[1:])
            else:
                # content can be empty if message consists of only command
                self.content = None
