
def _weak_or_strong_ref(func, callback):
    """
    Return a `WeakMethod` wrapping *func* if possible, else a `_StrongRef`.
    """
    try:
        return weakref.WeakMethod(func, callback)
    except TypeError:
        return _StrongRef(func)

