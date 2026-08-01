
def _wait_all_workers(timeout=DEFAULT_SHUTDOWN_TIMEOUT):
    r"""
    Block until all local and remote RPC processes reach this method and wait
    for all outstanding work to complete. Every RPC process must call this
    method before exit to perform a graceful shutdown. This should be used to
    terminate the RPC framework, and there is no guarantee that the RPC
    framework will work after this method returns.
    """
    try:
        _all_gather(None, timeout=timeout)
    except RuntimeError as ex:
        logger.exception("Failed to respond to 'Shutdown Proceed' in time")
        raise ex

