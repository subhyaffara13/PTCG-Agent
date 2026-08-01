
def mycallersname():
    """Returns the name of the caller of the caller of this function
    (hence the name of the caller of the function in which
    "mycallersname()" textually appears).  Returns None if this cannot
    be determined."""

    # http://docs.python.org/library/inspect.html#the-interpreter-stack
    import inspect

    frame = inspect.currentframe()
    if not frame:
        return None
    frame_, filename_, lineno_, funname, linelist_, listi_ = inspect.getouterframes(
        frame
    )[2]
    return funname

