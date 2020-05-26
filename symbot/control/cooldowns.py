from time import time


class Cooldowns:
    """Controller class to keep track of command cooldowns

    Attributes
    ----------
    cooldowns : dict([Command, float])
        dict to keep track of command cooldowns

    Methods
    -------
    has_cooldown
        determine whether a command is on cooldown
    """

    def __init__(self):
        self.cooldowns = dict()

    def has_cooldown(self, command, msg_timestamp):
        """determine whether a command is on cooldown

        Parameters
        ----------
        command : Command
            command to be checked for cooldown
        msg_timestamp : float
            epoch time of message

        Returns
        -------
        bool
            command is on cooldown
        """

        # check for existing entry
        if self.cooldowns[command]:
            # determine whether enough time has passed since last call
            if self.cooldowns[command] - msg_timestamp < command.cooldown:
                return True
        # if command was not on cooldown, put on cooldown
        self.cooldowns[command] = time()
        return False
