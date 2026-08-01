
def _iszero(x):
    """Returns True if x is zero."""
    return x.is_zero


def _iszero(x):
    """Returns True if x is zero."""
    return getattr(x, 'is_zero', None)

