
def get_int_opt(options, optname, default=None):
    """As :func:`get_bool_opt`, but interpret the value as an integer."""
    string = options.get(optname, default)
    try:
        return int(string)
    except TypeError:
        raise OptionError(f'Invalid type {string!r} for option {optname}; you '
                          'must give an integer value')
    except ValueError:
        raise OptionError(f'Invalid value {string!r} for option {optname}; you '
                          'must give an integer value')


def get_int_opt(options, optname, default=None):
    """As :func:`get_bool_opt`, but interpret the value as an integer."""
    string = options.get(optname, default)
    try:
        return int(string)
    except TypeError:
        raise OptionError(f'Invalid type {string!r} for option {optname}; you '
                          'must give an integer value')
    except ValueError:
        raise OptionError(f'Invalid value {string!r} for option {optname}; you '
                          'must give an integer value')

