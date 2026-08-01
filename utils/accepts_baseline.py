
def accepts_baseline(*args):
    """Decorator to indicate formatter accepts baseline results

    Use of this decorator before a formatter indicates that it is able to deal
    with baseline results.  Specifically this means it has a way to display
    candidate results and know when it should do so.
    """

    def wrapper(func):
        if not hasattr(func, "_accepts_baseline"):
            func._accepts_baseline = True

        LOG.debug("accepts_baseline() decorator executed on %s", func.__name__)

        return func

    return wrapper(args[0])

