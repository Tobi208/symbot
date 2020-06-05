import json
import logging
import os


class Settings:
    """Controller class to override default command settings

    Attributes
    ----------
    commands : dict
        commands loaded by central control
    file_path : str
        path of datafile
    settings : dict
        dict to store command settings

    Methods
    -------
    override
        override default settings from devs with user settings
    set_attr
        set an attribute of a command
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

        logging.info('overriding default command settings with user settings')
        # for each cmd_name, look up its settings
        for cmd_name, setting in self.settings.items():
            # and override the command attr for each altered attr
            for attr, val in setting.items():
                self.set_attr(cmd_name, attr, val)

    def set_attr(self, cmd_name, attr, val):
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

        command = self.commands[cmd_name]

        try:
            cmd_attr = command.__getattribute__(attr)
            # enforce that val has to be same type as cmd_attr
            if type(cmd_attr) == type(val):
                # set attribute to val
                command.__setattr__(attr, val)
            else:
                logging.info(f'{cmd_name} unable to set '
                             f'{attr}, because '
                             f'{val} is of type '
                             f'{type(val)} instead of type'
                             f'{type(cmd_attr)}')
        except AttributeError:
            logging.info(f'{cmd_name} unable to set '
                         f'{attr}, because '
                         f'command has no such attribute')
