
def errors(obj, depth=0, exact=False, safe=False):
    """get errors for objects that fail to pickle"""
    from dill import pickles, copy
    if not depth:
        try:
            pik = copy(obj)
            if exact:
                assert pik == obj, \
                    "Unpickling produces %s instead of %s" % (pik,obj)
            assert type(pik) == type(obj), \
                "Unpickling produces %s instead of %s" % (type(pik),type(obj))
            return None
        except Exception:
            import sys
            return sys.exc_info()[1]
    _dict = {}
    for attr in dir(obj):
        try:
            _attr = getattr(obj,attr)
        except Exception:
            import sys
            _dict[attr] = sys.exc_info()[1]
            continue
        if not pickles(_attr,exact,safe):
            _dict[attr] = errors(_attr,depth-1,exact,safe)
    return _dict


def errors(request):
    return request.param

