import json
import os


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

        # load environment from data folder
        # MAYBE put path into config or somewhere else
        with open(f'{os.getcwd()[:-6]}data{os.sep}environment.json') as file:
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
        return self.environment[var]
