
def strptime(s, fmt=None):
    """
    This function is available in the datetime module only from Python >=
    2.5.

    """
    if isinstance(s, bytes):
        s = s.decode("latin1")
    return datetime(*time.strptime(s, fmt)[:3])

