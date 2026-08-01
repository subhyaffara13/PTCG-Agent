
def takes_config(*args):
    """Test function takes config

    Use of this delegate before a test function indicates that it should be
    passed data from the config file. Passing a name parameter allows
    aliasing tests and thus sharing config options.
    """
    name = ""

    def _takes_config(func):
        if not hasattr(func, "_takes_config"):
            func._takes_config = name
        return func

    if len(args) == 1 and callable(args[0]):
        name = args[0].__name__
        return _takes_config(args[0])
    else:
        name = args[0]
        return _takes_config

