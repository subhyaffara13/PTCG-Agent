
def outermost(func): # is analogous to getsource(func,enclosing=True)
    """get outermost enclosing object (i.e. the outer function in a closure)

    NOTE: this is the object-equivalent of getsource(func, enclosing=True)
    """
    if ismethod(func):
        _globals = func.__func__.__globals__ or {}
    elif isfunction(func):
        _globals = func.__globals__ or {}
    else:
        return #XXX: or raise? no matches
    _globals = _globals.items()
    # get the enclosing source
    from .source import getsourcelines
    try: lines,lnum = getsourcelines(func, enclosing=True)
    except Exception: #TypeError, IOError
        lines,lnum = [],None
    code = ''.join(lines)
    # get all possible names,objects that are named in the enclosing source
    _locals = ((name,obj) for (name,obj) in _globals if name in code)
    # now only save the objects that generate the enclosing block
    for name,obj in _locals: #XXX: don't really need 'name'
        try:
            if getsourcelines(obj) == (lines,lnum): return obj
        except Exception: #TypeError, IOError
            pass
    return #XXX: or raise? no matches

