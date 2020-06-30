from symbot.util.strings import stringify


class Builder:
    """



    """

    def __init__(self, control):
        self.control = control

    def build_command(self, skeleton):
        print(self.assemble(skeleton))

    def assemble(self, skeleton):

        # header always the same
        code = \
            'import logging\n' \
            '\n' \
            'from symbot.chat.message import Message\n' \
            'from symbot.control.control import Control\n' \
            'from symbot.dev.commands._base_command import BaseCommand\n' \
            '\n' \
            'class Command(BaseCommand):\n' \
            '\n' \
            '    def __init__(self, control: Control):\n' \
            '        super().__init__(control)\n'

        # skeleton = {
        #     'r': [],
        #     'v': [],
        #     'c': [],
        #     'a': [],
        #     'u': [],
        #     'alias': [],
        #     'settings': {'name': stringify(name), 'author': stringify(msg.user)}
        # }

        # override default settings
        for setting, value in skeleton['settings'].items():
            code += \
                f'        self.{setting} = {value}\n'

        code += \
            '\n' \
            '    async def run(self, msg: Message):\n' \
            '\n'

        # adjust message according to alias
        for alias in skeleton['alias']:
            code +=\
                '\n' \
                f'msg.command = {alias}\n' \
                '\n' \
                'await self.control.requeue(msg)\n'

        # aliases are special case
        # ignore everything else and
        # only execute aliases
        # MAYBE change in the future
        if len(skeleton['alias']) > 0:
            return code

        # initialize var if it does not exist
        # increment vars
        for var in skeleton['c']:
            self.control.environment.initialize(var)
            code += \
                '        try:\n' \
                f'            {var} = self.control.environment.increment({stringify(var)})\n' \
                '        except KeyError:\n' \
                f'            logging.info(f\'{{self.name}} unable to find var {var}\')\n' \
                '            return\n'

        # initialize var if it does not exist
        # retrieve vars
        for var in skeleton['v']:
            self.control.environment.initialize(var)
            code += \
                '        try:\n' \
                f'            {var} = self.control.environment.get({stringify(var)})\n' \
                '        except KeyError:\n' \
                f'            logging.info(f\'{{self.name}} unable to find var {var}\')\n' \
                '            return\n'

        # retrieve arguments from message
        for i, arg in enumerate(skeleton['a']):
            code += \
                '        try:\n' \
                f'            {arg} = msg.context[{i}]\n' \
                '        except IndexError:\n' \
                f'            logging.info(f\'{{self.name}} missing context {arg}\')\n' \
                '            return\n'

        # retrieve user from message
        for user in skeleton['u']:
            code += \
                f'        {user} = msg.user\n'

        # generate response
        response = ''.join(skeleton['r'])
        code += \
            '\n' \
            f'        response = f\'{response}\n'

        # respond to control
        code += \
            '        await self.control.respond(response)'

        return code
