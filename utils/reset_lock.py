
def reset_lock():
    """Reset the global lock.

    This should be called only on the init of a forked process to reset the lock to
    None, enabling the new forked process to get a new lock.
    """
    global _lock

    iothread[0] = None
    loop[0] = None
    _lock = None

