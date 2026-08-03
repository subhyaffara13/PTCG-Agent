from typing import Any

def getargspec(f):
    """A replacement for inspect.getargspec"""
    spec = getfullargspec(f)
    return ArgSpec(spec.args, spec.varargs, spec.varkw, spec.defaults)


def getargspec(func: Any) -> inspect.FullArgSpec:
    """Like inspect.getargspec but supports functools.partial as well."""
    if inspect.ismethod(func):
        func = func.__func__
    if type(func) is partial:
        orig_func = func.func
        argspec = getargspec(orig_func)
        args = list(argspec[0])
        defaults = list(argspec[3] or ())
        kwoargs = list(argspec[4])
        kwodefs = dict(argspec[5] or {})
        if func.args:
            args = args[len(func.args) :]
        for arg in func.keywords or ():
            try:
                i = args.index(arg) - len(args)
                del args[i]
                try:
                    del defaults[i]
                except IndexError:
                    pass
            except ValueError:  # must be a kwonly arg
                i = kwoargs.index(arg)
                del kwoargs[i]
                del kwodefs[arg]
        return inspect.FullArgSpec(
            args, argspec[1], argspec[2], tuple(defaults), kwoargs, kwodefs, argspec[6]
        )
    while hasattr(func, "__wrapped__"):
        func = func.__wrapped__
    if not inspect.isfunction(func):
        raise TypeError("%r is not a Python function" % func)
    return inspect.getfullargspec(func)


def getargspec(func):
    """Get the names and default values of a function's arguments.

    A tuple of four things is returned: (args, varargs, varkw, defaults).
    'args' is a list of the argument names (it may contain nested lists).
    'varargs' and 'varkw' are the names of the * and ** arguments or None.
    'defaults' is an n-tuple of the default values of the last n arguments.

    """

    if ismethod(func):
        func = func.__func__
    if not isfunction(func):
        raise TypeError('arg is not a Python function')
    args, varargs, varkw = getargs(func.__code__)
    return args, varargs, varkw, func.__defaults__

