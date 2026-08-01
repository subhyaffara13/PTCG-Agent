
def check_non_empty(key, value):
    """Raise a TypeError if an empty sequence is passed"""
    if (not cbook.is_scalar_or_string(value) and
            isinstance(value, collections.abc.Sized) and len(value) == 0):
        raise TypeError(f'{key} must not be an empty sequence')

