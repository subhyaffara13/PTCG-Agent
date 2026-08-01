
def _create_weakref(obj, *args):
    from weakref import ref
    if obj is None: # it's dead
        from collections import UserDict
        return ref(UserDict(), *args)
    return ref(obj, *args)

