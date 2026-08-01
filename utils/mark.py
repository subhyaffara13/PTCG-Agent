
def mark(msg):
    """
    Describe an instantaneous event that occurred at some point.

    Args:
        msg (str): ASCII message to associate with the event.
    """
    return _nvtx.markA(msg)


def mark(msg):
    """
    Describe an instantaneous event that occurred at some point.

    Arguments:
        msg (str): ASCII message to associate with the event.
    """
    return _itt.mark(msg)

