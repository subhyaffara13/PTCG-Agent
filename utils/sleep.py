
def sleep(seconds: float) -> None:
    """
    Sleep strategy that delays execution for a given number of seconds.

    This is the default strategy, and may be mocked out for unit testing.
    """
    time.sleep(seconds)


def sleep(t):
    time.sleep(t)

