import json
import logging
import os


class Settings:
    """Controller class to override default command settings

    Attributes
    ----------
    commands : list
        commands loaded by central control
    file_path : str
        path of datafile
    settings : dict
        dict to store command settings

    Methods
    -------
    override
        override default settings from devs with user settings
    """

    def __init__(self, commands):
        self.commands = commands

        # MAYBE put path into config or somewhere else
        self.file_path = f'{os.getcwd()[:-6]}data{os.sep}command_settings.json'

        # load command settings from data folder
        try:
            logging.info('loading command settings')
            with open(self.file_path) as file:
                self.settings = json.load(file)
        # or start fresh command settings
        except FileNotFoundError:
            logging.info(f'no command settings found in {self.file_path}')
            self.settings = {}
            logging.info('created new command settings')

        # override default settings with user settings
        self.override()

    def override(self):
        """override default settings from devs with user settings"""
        pass

    def set(self, cmd_name, attr, val):
        """set an attribute of a command

        Parameters
        ---------
        cmd_name : str
            command identifier
        attr : str
            attribute to be set
        val : object
            value to be assigned
        """
        pass
