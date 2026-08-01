
def _call_callback_maybe_halt(callback, res):
    """Call wrapped callback; return True if algorithm should stop.

    Parameters
    ----------
    callback : callable or None
        A user-provided callback wrapped with `_wrap_callback`
    res : OptimizeResult
        Information about the current iterate

    Returns
    -------
    halt : bool
        True if minimization should stop

    """
    if callback is None:
        return False
    try:
        callback(res)
        return False
    except StopIteration:
        callback.stop_iteration = True
        return True

