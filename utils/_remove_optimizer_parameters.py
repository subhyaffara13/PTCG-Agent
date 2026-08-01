
def _remove_optimizer_parameters(kwds):
    """
    Remove the optimizer-related keyword arguments 'loc', 'scale' and
    'optimizer' from `kwds`.  Then check that `kwds` is empty, and
    raise `TypeError("Unknown arguments: %s." % kwds)` if it is not.

    This function is used in the fit method of distributions that override
    the default method and do not use the default optimization code.

    `kwds` is modified in-place.
    """
    kwds.pop('loc', None)
    kwds.pop('scale', None)
    kwds.pop('optimizer', None)
    kwds.pop('method', None)
    if kwds:
        raise TypeError(f"Unknown arguments: {kwds}.")

