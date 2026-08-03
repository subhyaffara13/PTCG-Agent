from typing import Callable

def _start_event_loop_in_thread(
    event_loop: asyncio.AbstractEventLoop, call_soon_cb: Callable, *args
):
    """
    Starts event loop in a thread and schedule callback as soon as event loop is ready.
    Used to be able to schedule tasks using loop.call_later.

    :param event_loop:
    :return:
    """
    asyncio.set_event_loop(event_loop)
    event_loop.call_soon(call_soon_cb, event_loop, *args)
    try:
        event_loop.run_forever()
    finally:
        try:
            # Clean up pending tasks
            pending = asyncio.all_tasks(event_loop)
            for task in pending:
                task.cancel()
            # Run loop once more to process cancellations
            event_loop.run_until_complete(
                asyncio.gather(*pending, return_exceptions=True)
            )
        except Exception:
            pass
        finally:
            event_loop.close()

