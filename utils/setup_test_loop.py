
def setup_test_loop(
    loop_factory: _LOOP_FACTORY = asyncio.new_event_loop,
) -> asyncio.AbstractEventLoop:
    """Create and return an asyncio.BaseEventLoop instance.

    The caller should also call teardown_test_loop,
    once they are done with the loop.
    """
    loop = loop_factory()
    asyncio.set_event_loop(loop)
    return loop

