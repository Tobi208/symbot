import asyncio
import logging
import os
from importlib import import_module

from symbot.control.auxiliary.cooldowns import Cooldowns
from symbot.control.auxiliary.environment import Environment
from symbot.control.auxiliary.permissions import Permissions


class Control:
    """Central control element

    Controller communicates between Twitch chat, various data files,
    media elements and command calls & responses. Dynamically loads
    commands from control.commands and utilizes auxiliary controllers.

    Attributes
    ----------
    permissions : Permissions
        checks user permission levels
    environment : Environment
        manages environmental variables
    cooldowns : Cooldowns
        tracks command cooldowns
    commands : list
        list of all commands loaded dynamically
    msg_queue : Queue
        thread safe queue to receive Twitch messages
    resp_queue : Queue
        thread safe queue to push responses to

    Methods
    -------
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

        # auxiliary controllers
        self.permissions = Permissions()
        self.environment = Environment()
        self.cooldowns = Cooldowns()

        # dynamically load in commands
        self.commands = []
        # MAYBE make path dynamic
        logging.info('loading user commands')
        for file in os.listdir(f'dev{os.sep}commands'):
            # exclude files not meant to be loaded
            if not file.startswith('_'):
                # MAYBE make package dynamic
                module = import_module(f'symbot.dev.commands.{file[:-3]}')
                self.commands.append(module.Command(self))

        # async data structures
        self.msg_queue = None
        self.resp_queue = asyncio.Queue()

    def get_command(self, name):
        """try to find command by name

        Parameters
        ----------
        name : str
            command identifier

        Returns
        -------
        Command
            desired command, or None if not found
        """

        for command in self.commands:
            if name == command.name:
                return command
        return None

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

        # run forever
        while True:
            # wait for message to process
            # provided by chat
            msg = await self.msg_queue.get()
            command = self.get_command(msg.command)
            # check for existence
            if not command:
                continue
            # check for permission
            if not self.permissions.check(command.permission_level, msg.user):
                logging.info(
                    f'({msg.user})'
                    f' has insufficient permission to call '
                    f'({command.name})'
                )
                continue
            # check for cooldown
            if self.cooldowns.has_cooldown(command, msg.timestamp):
                logging.info(f'({command.name}) is still on cooldown')
                continue
            # command is safe to execute
            # append command to asyncio loop
            asyncio.get_running_loop().create_task(command.run(msg))
