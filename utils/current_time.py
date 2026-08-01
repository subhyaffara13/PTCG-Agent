
def current_time(lst):
    return timestampNow()


def current_time() -> float:
    """
    Return the current value of the event loop's internal clock.

    :return: the clock value (seconds)
    :raises NoEventLoopError: if no supported asynchronous event loop is running in the
        current thread

    """
    return get_async_backend().current_time()

