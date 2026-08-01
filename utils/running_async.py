
def running_async() -> bool:
    """Being executed by an event loop?"""
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False

