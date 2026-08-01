
def _create_weakproxy(obj, callable=False, *args):
    from weakref import proxy
    if obj is None: # it's dead
        if callable: return proxy(lambda x:x, *args)
        from collections import UserDict
        return proxy(UserDict(), *args)
    return proxy(obj, *args)

