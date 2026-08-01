
def _get_namespace(m):
    """
    This is used by _lambdify to parse its arguments.
    """
    if isinstance(m, str):
        _import(m)
        return MODULES[m][0]
    elif isinstance(m, dict):
        return m
    elif hasattr(m, "__dict__"):
        return m.__dict__
    else:
        raise TypeError("Argument must be either a string, dict or module but it is: %s" % m)

