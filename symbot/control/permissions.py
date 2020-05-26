import json
import os


class Permissions:
    """Controller class for user permission levels

    user permission levels as of now:
        0 : broadcaster
        1 : moderator
        2 : whitelisted
        3 : unregistered
        4 : blacklisted

    Attributes
    ----------
    permissions : dict
        dict to store user permission levels

    Methods
    -------
    check
        determine whether user has sufficient permission
    """

    def __init__(self):

        # load permissions from data folder
        # MAYBE put path into config or somewhere else
        with open(f'{os.getcwd()[:-6]}data{os.sep}environment.json') as file:
            self.permissions = json.load(file)

    def check(self, cmd_level, user):
        """determine whether user has sufficient permission

        Parameters
        ----------
        cmd_level : int
            minimum permission level required by command
        user : str
            user name

        Returns
        -------
        bool
            user has sufficient permission
        """

        if user in self.permissions:
            # get user level from data
            user_level = self.permissions[user]
        else:
            # or use default permission level
            # MAYBE enable dynamic user levels from config
            # MAYBE use enumerate?
            user_level = 3
        return user_level <= cmd_level
