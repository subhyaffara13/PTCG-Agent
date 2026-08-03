import sys

def print_function(print_cls):
    """ A decorator to replace kwargs with the printer settings in __signature__ """
    def decorator(f):
        if sys.version_info < (3, 9):
            # We have to create a subclass so that `help` actually shows the docstring in older Python versions.
            # IPython and Sphinx do not need this, only a raw Python console.
            cls = type(f'{f.__qualname__}_PrintFunction', (_PrintFunction,), {"__doc__": f.__doc__})
        else:
            cls = _PrintFunction
        return cls(f, print_cls)
    return decorator

