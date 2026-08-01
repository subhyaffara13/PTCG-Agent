
def _update_args(args, key, value):
    """Add a new ``(key, value)`` pair to arguments ``dict``. """
    args = dict(args)

    if key not in args:
        args[key] = value

    return args

