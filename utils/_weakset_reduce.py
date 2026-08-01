
def _weakset_reduce(obj):
    return weakref.WeakSet, (list(obj),)

