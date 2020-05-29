import json
import os

from symbot.util.updater import update_json


class Environment:
    """Controller class for Twitch chat's environmental variables

    Attributes
    ----------
    environment : dict
        dict to store environmental variables

    Methods
    -------
    get
        get the value of a variable
    set
        set the value of a variable
    increment
        increment the value of a variable
    """

    def __init__(self):

        # MAYBE put path into config or somewhere else
        self.file_path = f'{os.getcwd()[:-6]}data{os.sep}environment.json'

        # load environment from data folder
        with open(self.file_path) as file:
            self.environment = json.load(file)

    def get(self, var):
        """get the value of a variable

        Parameters
        ----------
        var : str
            variable name identifying desired value

        Returns
        -------
        object
            desired value
        """

        # MAYBE handle var not defined
        return self.environment[var]

    def set(self, var, val):
        """set the value of a variable

        Parameters
        ----------
        var : str
            variable name identifying value
        val : object
            value to be set

        Returns
        -------
        object
            set value
        """

        # MAYBE handle var not defined
        self.environment[var] = val
        update_json(self.environment, self.file_path)
        return val

    def increment(self, var):
        """increment the value of a variable

        Parameters
        ----------
        var : str
            variable name identifying value to be incremented

        Returns
        -------
        int
            incremented value
        """

        # MAYBE handle var not defined
        self.environment[var] += 1
        update_json(self.environment, self.file_path)
        return self.environment[var]
