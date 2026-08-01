
def getloadavg():
    """Return the number of processes in the system run queue averaged
    over the last 1, 5, and 15 minutes respectively as a tuple.
    """
    global _loadavg_initialized

    if _loadavg_initialized:
        return _getloadavg_impl()

    with _lock:
        if not _loadavg_initialized:
            cext.init_loadavg_counter()
            _loadavg_initialized = True

    return _getloadavg_impl()

