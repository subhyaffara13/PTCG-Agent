
def loop_context(
    loop_factory: _LOOP_FACTORY = asyncio.new_event_loop, fast: bool = False
) -> Iterator[asyncio.AbstractEventLoop]:
    """A contextmanager that creates an event_loop, for test purposes.

    Handles the creation and cleanup of a test loop.
    """
    loop = setup_test_loop(loop_factory)
    yield loop
    teardown_test_loop(loop, fast=fast)

