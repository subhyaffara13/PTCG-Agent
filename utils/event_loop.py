
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

