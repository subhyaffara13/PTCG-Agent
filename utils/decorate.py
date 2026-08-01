
def decorate(func, caller):
    """
    decorate(func, caller) decorates a function using a caller.
    """
    evaldict = dict(_call_=caller, _func_=func)
    fun = FunctionMaker.create(
        func, "return _call_(_func_, %(shortsignature)s)",
        evaldict, __wrapped__=func)
    if hasattr(func, '__qualname__'):
        fun.__qualname__ = func.__qualname__
    return fun

