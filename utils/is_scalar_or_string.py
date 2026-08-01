
def is_scalar_or_string(val):
    """Return whether the given object is a scalar or string like."""
    return isinstance(val, str) or not np.iterable(val)

