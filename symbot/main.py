import asyncio

from symbot.chat.chat import Chat
from symbot.control.control import Control


async def main():
    chat = Chat()
    control = Control()
    control.msg_queue = chat.msg_queue
    chat.resp_queue = control.resp_queue

    await chat.open_connection()
    await asyncio.gather(chat.read(), control.process(), chat.write())


asyncio.run(main())
