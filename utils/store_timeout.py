
def store_timeout(store, timeout: float):
    """
    This sets the timeout and then restores the old timeout when the context
    manager exits.

    Args:
        store: the store to set the timeout on
        timeout: the timeout to set
    """

    old_timeout = store.timeout
    store.set_timeout(timedelta(seconds=timeout))
    yield
    store.set_timeout(old_timeout)

