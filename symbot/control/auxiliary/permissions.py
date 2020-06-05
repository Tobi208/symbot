import json
import os

from symbot.util.updater import update_json


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
    file_path : str
        path of datafile
    permissions : dict
        dict to store user permission levels

    Methods
    -------
    set
        assign permission level to a user
    check
        determine whether user has sufficient permission
    """

    def __init__(self):

        # MAYBE put path into config or somewhere else
        self.file_path = f'{os.getcwd()[:-6]}data{os.sep}permissions.json'

        # load permissions from data folder
        with open(self.file_path) as file:
            self.permissions = json.load(file)

    def set(self, user, level):
        """assign permission level to a user

        Parameters
        ----------
        user : str
            user identifier
        level : int
            permission level
        """

        if level == 3:
            del self.permissions[user]
        else:
            self.permissions[user] = level
        update_json(self.permissions, self.file_path)

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
