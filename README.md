# Symbot
A python twitch chat bot based on asyncio.

This versatile chat bot lets broadcasters with a general understanding of the python language fully customize the chat experience for their viewers.
It functions as a framework that can be built upon as desired with new commands and media types.
Due to its highly encapsulated structure, new additions can be effortlessly shared with other broadcasters.
For broadcasters without any programming knowledge, this chat bot still provides most functionalities that popular chat bots such as _nightbot_ offer too.

### Getting Started

1. Symbot requires ``Python 3.7`` or newer, but only uses the standard library.
2. ``pip install symbot``
3. Get your [Twitch API Key](https://twitchapps.com/tmi/).
4. Enter your channel name, name of your bot and your key in ``config.py``.
5. Enter yourself as ``"broadcaster" : "<name>"`` in ``environment.json``.
6. Give yourself and your bot permission level ``0`` in ``user_permissions.json``.
7. Become familiar with the ``meta commands``.
8. ``python -m symbot``

### Meta Commands

---
#### !command

This is the central tool to manage your commands through chat.

> !command (operation) (name) (content) (settings)

``operation`` has to be ``add``, ``edit`` or ``del``.
The ``add`` operation requires you to enter ``content``, while ``edit`` can change the ``content`` and ``settings`` or only the ``settings`` of a command. 
``del`` only requires the name of the command.

``name`` does not require a prefix. ``!hey`` works as well as ``hey``.

```content``` specifies what response the command will send to your chat. It can be arbitrary text such as ``Hello there!``, but you may also use special functions.
This includes:

Function | Usage | Description
------|--------|-------
variable | ``$v{var}`` | Looks up a variable in ``environment.json`` and returns its value.
counter | ``$c{var}`` | Looks up a variable in ``environment.json``, increments it and returns its new value.
argument | ``$a{arg}`` | Specifies an argument that is passed when the command is called.
user | ``$u{user}`` | Returns the user name who called the command.
alias | ``$alias{command}`` | Does the same as another command.

Furthermore you can directly manipulate the general ``settings`` of a command with the following:

Setting | Usage | Values | Description
------|--------|----|---
permission level | ``-ul=val`` | ``0,1,2,3,4`` | The required user permission level to call this command.
cooldown | ``-cd=val`` | positive integer | The minimum amount of time that has to pass between two command calls in seconds.
enabled | ``-on=val`` | ``true,false`` | Specifically enable or disable this command in general.

Be aware, that these are *general* settings, which are different from *user specific* settings. This will be explained in the description of the corresponding meta commands.
``settings`` are optional. They will be set to a default value if not specified, so do not change them unless it serves a purpose.

Example | Usage | Response
--------|-------|---------
``!command add !new this is a new command`` | !new | _this is a new command_
``!command add !name my name is $v{broadcaster}`` | !name | _my name is Jane Doe_
``!command add !count this command has been used $c{count} times`` | !count | _this command has been used 1 times_
``!command add !highfive $u{donor} gave $a{receptor} a virtual highfive`` | !highfive herself | _Jane Doe gave herself a virtual highfive_
``!command add !neu $alias{!new}`` | !neu | _this is a new command_
``!command add !cd you can do this every 5 seconds -cd=5`` | !cd | _you can do this every 5 seconds_
``!command add !cd try again in 5 seconds`` | !cd | _try again in 5 seconds_
``!command edit !cd try again in 10 seconds -cd=10`` | !cd | _try again in 10 seconds_
``!command edit !cd -on=false`` | !cd | 
``!command del !name`` | !name |

---
#### !var

Manipulate your ``environment``. Sometimes you want to directly change or retrieve a variable through chat.

> !var (operation) (variable) (value)

``operation`` has to be ``get``, ``set`` or ``del``. Only ``set`` requires you to pass a value. New values will be tried to cast to the same type as the old value.
Functions such as ``count`` require a certain value type (integer), so changing the type of a value my affect commands.

Example | Usage | Response
--------|-------|---------
``!var get broadcaster`` | | _broadcaster has value Jane Doe_
``!var set count 20`` | !count | _this command has been used 21 times_
``!var del count`` | !count | _Error: variable count not found_

---
#### !setcmdsetting

Manage your user settings in ``command_settings``.

> !setcmdsetting (setting) (value)

Changes made to your user settings only apply to your personal bot instance,
so please use ``!setcmdsetting`` instead of ``!command edit`` to change settings.
This makes sharing commands with other broadcasters easier.

Setting | Value | Description
--------|------|-------------
name | ``str`` | If you want to change how a command is called.
author | ``str`` | Technically only for ``!purge`` yet.
permission_level | ``0,1,2,3,4`` | The required user permission level to call this command.
cooldown | ``int`` | The minimum amount of time that has to pass between two command calls in seconds.
enabled | ``bool`` | Temporarily enable or disable a command. Does *not* delete it.

---
#### !setuserperm

Manage your user permission levels in ``user_permissions``.

> !setuserperm (user) (value)

``permission levels`` are used to control who can do what. Meta commands generally have a permission level of ``1``, while standard commands have permission level ``3``.
Permission levels ``2,4`` may be used to permit the usage of abusable commands or deny command spammers.
Certain actions such as deleting commands require a more powerful level.

Level | Group | Description
------|-------|-------------
0 | Broadcaster | Most powerful level, has full control over everything.
1 | Moderator | Has control over most meta commands.
2 | Allowed | Has control over abusable commands, broadcaster trusts this person.
3 | Casual | Default user level. May use all standard commands.
4 | Blocked | Is blocked from using most commands.


---
#### !purge

Delete all commands created by a user.

> !purge (user)

This exists in case you look away for a couple of minutes and someone with ill intend created a bunch of questionable commands that now need to be deleted.
You will be glad you can deleted them all with a single command.
Only usable with permission level ``0``.


### Develop

If you are interested in building new things in this framework, pay attention to the ``dev`` package.

``commands`` is the main bulk.
In there are all the standard commands that are added, edited and deleted through chat.
Commands are automatically generated python modules that are loaded in dynamically.
You may change them here directly or create new ones manually.
The automatically generated commands serve as a good vantage point on how to create new commands manually.
Although ``Exceptions`` from command calls can not crash the program, because they are 'stuck' in a coroutine, it would be great to avoid them and log what's going on.
Become familiar with the ``control`` elements and what functionalities they provide.

``meta`` contains all meta command that manipulate commands and environments.
They are more complex than standard commands and produced manually.
An understanding of the entire structure is required to write new meta commands.

``media`` is the biggest remaining construction site right now.
Future additions may contain usage of text files, sound files, video files, polls, text to speech, API calls and more.
Media modules can be used by commands to generate an effect or response.

The framework may require expansion for more complex features and is subject to change.
This project is far from complete, but it is fully functional as it is.

Please report any bugs or concerns.

### Future todos and command or media ideas
- add a cli
- add graceful ctrl+C shutdown
- add demo mode
- enable/disable packages
- track command usage with new aux controller
- proper user interface
- automatically set up broadcaster & bot permissions
- add setvar as a content functionality
- song requests
- on screen counter
- text to speech
- play sound
- play video
- poll
- repeating commands
- proper list of commands
- cleanup environment unused vars
- temporarily change user permission
- proper moderation commands