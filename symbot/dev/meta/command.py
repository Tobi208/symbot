import logging
import re

from symbot.chat.message import Message
from symbot.dev.meta._base_meta_command import BaseMetaCommand
from symbot.dev.meta._builder import Builder
from symbot.util.strings import stringify


class Command(BaseMetaCommand):

    def __init__(self, control):
        super().__init__(control)
        self.name = '!command'
        self.author = 'fd_symbicort'

        self.builder = Builder(control)

        self.arg_extractor = re.compile('\\$(.*){(.*)}')
        self.setting_extractor = re.compile('-(.*)=(.*)')

    async def run(self, msg: Message):

        try:
            operation = msg.context[0]
        except IndexError:
            logging.info('!command missing operation argument')
            return

        if operation == 'add':
            await self.addcom(msg)
        elif operation == 'edit':
            await self.editcom(msg)
        elif operation == 'del':
            await self.delcom(msg)
        else:
            logging.info(f'!command encountered an undefined operation argument {operation}')

    async def addcom(self, msg):

        try:
            name = msg.context[1]
        except IndexError:
            logging.info('!command add missing command name argument')
            return
        if self.control.get_command(name):
            logging.info(f'!command add {name} already exists')
            return
        try:
            msg.context[2]
        except IndexError:
            logging.info(f'!command add {name} missing content')
            return

        skeleton = {
            'r': [],
            'v': [],
            'c': [],
            'a': [],
            'u': [],
            'alias': [],
            'settings': {'name': stringify(name), 'author': stringify(msg.user)}
        }

        for s in msg.context[2:]:
            if s.startswith('$'):
                try:
                    arg, value = self.arg_extractor.search(s).groups()
                    skeleton[arg].append(value)
                    skeleton['r'].append('{' + value + '}')
                except AttributeError:
                    logging.info(f'!command add {name} has bad argument')
                    return
                except KeyError:
                    logging.info(f'!command add {name} encountered undefined argument')
                    return
            elif s.startswith('-'):
                try:
                    setting, value = self.setting_extractor.search(s).groups()
                    if setting == 'ul':
                        skeleton['settings']['permission_level'] = int(value)
                    elif setting == 'cd':
                        skeleton['settings']['cooldown'] = float(value)
                    elif setting == 'id':
                        skeleton['settings']['name'] = value
                    elif setting == 'on':
                        skeleton['settings']['enabled'] = value.lower() == 'true'
                    else:
                        logging.info(f'!command add {name} invalid setting {setting}')
                        return
                except AttributeError:
                    logging.info(f'!command add {name} has bad setting')
                    return
                except ValueError:
                    logging.info(f'!command add {name} can not convert setting value')
                    return
            else:
                skeleton['r'].append(s)

        self.builder.create_command(skeleton)

    async def editcom(self, msg):
        pass

    async def delcom(self, msg):
        pass


# !commands:
#     !command add !commands https://github.com/tobi208/symbot#commands
#
# !deaths:
#     !command add !deaths $v{broadcaster} has died $v{deaths} times :(
#
# !geinted:
#     !command add !geinted $alias{!int}
#
# hey:
#     !command add hey Hey there, $u{recipient} HeyGuys
#
# !highfive:
#     !command add !highfive $u{user} hat $a{recipient} ein highfive gegeben?
#
# !int:
#     !command add !int $v{broadcaster} hat schon $c{bad} mal den turbo int rausgehauen
#
# warum:
#     !command add warum weil halt
#
