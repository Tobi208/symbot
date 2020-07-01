import asyncio
import logging
import os
from importlib import import_module

from symbot.control.auxiliary.cooldowns import Cooldowns
from symbot.control.auxiliary.environment import Environment
from symbot.control.auxiliary.permissions import Permissions
from symbot.control.auxiliary.settings import Settings


class Control:
    """Central control element

    Controller communicates between Twitch chat, various data files,
    media elements and command calls & responses. Dynamically loads
    commands from dev and utilizes auxiliary controllers.

    Attributes
    ----------
    permissions : Permissions
        checks user permission levels
    environment : Environment
        manages environmental variables
    cooldowns : Cooldowns
        tracks command cooldowns
    settings : Settings
        overrides default command settings
    commands : list
        dict of all commands loaded dynamically
    msg_queue : Queue
        thread safe queue to receive Twitch messages
    resp_queue : Queue
        thread safe queue to push responses to

    Methods
    -------
    import_commands
        recursively import and instantiate all commands in a directory
    get_command
        try to find command by name
    requeue
        push message back to message queue
    respond
        push response to response queue
    process
        continuously process messages from Twitch channel
    """

    def __init__(self):

        # dynamically load in commands
        self.commands = {}
        logging.info('loading commands')
        self.import_commands(f'dev{os.sep}commands')
        self.import_commands(f'dev{os.sep}meta')

        # auxiliary controllers
        self.permissions = Permissions()
        self.environment = Environment()
        self.cooldowns = Cooldowns()
        self.settings = Settings(self.commands)

        # async data structures
        self.msg_queue = None
        self.resp_queue = asyncio.Queue()

    def import_commands(self, path):
        """recursively import and instantiate all commands in a directory

        Parameters
        ----------
        path : str
            current directory of modules to be imported
        """

        for file in os.listdir(path):
            # exclude files not meant to be loaded
            if file.startswith('_'):
                continue
            # import .py modules
            elif file.endswith('.py'):
                package = '.'.join(path.split(os.sep))
                command = import_module(f'symbot.{package}.{file[:-3]}').Command(self)
                if command.name not in self.commands:
                    self.commands[command.name] = command
            # import modules from lower levels recursively
            else:
                self.import_commands(path + os.sep + file)

    def get_command(self, cmd_name):
        """try to find command by name

        Parameters
        ----------
        cmd_name : str
            command identifier

        Returns
        -------
        Command
            desired command, or None if not found
        """

        if cmd_name not in self.commands:
            return None
        return self.commands[cmd_name]

    async def requeue(self, msg):
        """push message back to message queue

        Parameters
        ----------
        msg : Message
            modified message that needs to be reprocessed
        """
        await self.msg_queue.put(msg)

    async def respond(self, response):
        """push response to response queue

        Parameters
        ----------
        response : str
            response to be sent to Twitch channel
        """

        await self.resp_queue.put(response)

    async def process(self):
        """continuously process messages from Twitch channel

        continuously process messages from Twitch channel. Check for
        various flags before executing a command. Not every command
        generates a response.
        """

        # from symbot.dev.meta.command import Command
        # from symbot.chat.message import Message
        # m = Message('bruh:bruh!bruh@bruh.tmi.twitch.tv PRIVMSG #fd_symbicort :!command add !ded $v{broadcaster} ist schon $c{deaths} mal brutalst verreckt -cd=5')
        # c = Command(self)
        # await c.run(m)

        # run forever
        while True:
            # wait for message to process
            # provided by chat
            msg = await self.msg_queue.get()
            command = self.get_command(msg.command)
            # check for existence
            if not command:
                continue
            # check if command is enabled
            if not command.enabled:
                logging.info(f'{command.name} is disabled')
                continue
            # check for permission
            if not self.permissions.check(command.permission_level, msg.user):
                logging.info(f'{msg.user} has insufficient permission to call {command.name}')
                continue
            # check for cooldown
            if self.cooldowns.has_cooldown(command, msg.timestamp):
                logging.info(f'{command.name} is still on cooldown')
                continue
            # command is safe to execute
            # append command to asyncio loop
            asyncio.get_running_loop().create_task(command.run(msg))
