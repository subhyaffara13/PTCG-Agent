
def _proxy_helper(obj): # a dead proxy returns a reference to None
    """get memory address of proxy's reference object"""
    _repr = repr(obj)
    try: _str = str(obj)
    except ReferenceError: # it's a dead proxy
        return id(None)
    if _str == _repr: return id(obj) # it's a repr
    try: # either way, it's a proxy from here
        address = int(_str.rstrip('>').split(' at ')[-1], base=16)
    except ValueError: # special case: proxy of a 'type'
        if not IS_PYPY:
            address = int(_repr.rstrip('>').split(' at ')[-1], base=16)
        else:
            objects = iter(gc.get_objects())
            for _obj in objects:
                if repr(_obj) == _str: return id(_obj)
            # all bad below... nothing found so throw ReferenceError
            msg = "Cannot reference object for proxy at '%s'" % id(obj)
            raise ReferenceError(msg)
    return address

