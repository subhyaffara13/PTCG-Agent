
def isarray(x):
    """Same as ``isinstance(x, array)``."""
    return isinstance(x, array)


def isarray(var):
    return 'dimension' in var and not isexternal(var)

