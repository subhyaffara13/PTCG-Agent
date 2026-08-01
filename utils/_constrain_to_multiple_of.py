
def _constrain_to_multiple_of(val, multiple, min_val=0, max_val=None):
    """Constrain a value to be a multiple of another value."""
    x = round(val / multiple) * multiple

    if max_val is not None and x > max_val:
        x = math.floor(val / multiple) * multiple

    if x < min_val:
        x = math.ceil(val / multiple) * multiple

    return x


def _constrain_to_multiple_of(val, multiple, min_val=0, max_val=None):
    """Constrain a value to be a multiple of another value."""
    x = round(val / multiple) * multiple

    if max_val is not None and x > max_val:
        x = math.floor(val / multiple) * multiple

    if x < min_val:
        x = math.ceil(val / multiple) * multiple

    return x

