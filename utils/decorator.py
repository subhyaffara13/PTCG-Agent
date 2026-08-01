
def decorator(caller, _func=None):
    """decorator(caller) converts a caller function into a decorator"""
    if _func is not None:  # return a decorated function
        # this is obsolete behavior; you should use decorate instead
        return decorate(_func, caller)
    # else return a decorator function
    if inspect.isclass(caller):
        name = caller.__name__.lower()
        doc = 'decorator(%s) converts functions/generators into ' \
              'factories of %s objects' % (caller.__name__, caller.__name__)
    elif inspect.isfunction(caller):
        if caller.__name__ == '<lambda>':
            name = '_lambda_'
        else:
            name = caller.__name__
        doc = caller.__doc__
    else:  # assume caller is an object with a __call__ method
        name = caller.__class__.__name__.lower()
        doc = caller.__call__.__doc__
    evaldict = dict(_call_=caller, _decorate_=decorate)
    return FunctionMaker.create(
        '%s(func)' % name, 'return _decorate_(func, _call_)',
        evaldict, doc=doc, module=caller.__module__,
        __wrapped__=caller)

