
def _wrapfunc(obj, method, *args, **kwds):
    bound = getattr(obj, method, None)
    if bound is None:
        return _wrapit(obj, method, *args, **kwds)

    try:
        return bound(*args, **kwds)
    except TypeError:
        # A TypeError occurs if the object does have such a method in its
        # class, but its signature is not identical to that of NumPy's. This
        # situation has occurred in the case of a downstream library like
        # 'pandas'.
        #
        # Call _wrapit from within the except clause to ensure a potential
        # exception has a traceback chain.
        return _wrapit(obj, method, *args, **kwds)

