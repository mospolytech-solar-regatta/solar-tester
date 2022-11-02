from listener.listener import Listener


async def get_listener():
    l = Listener()
    try:
        yield l
    except:
        await l.stop()
