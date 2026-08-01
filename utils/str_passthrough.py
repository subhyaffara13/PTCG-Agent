
def str_passthrough(obj):
    """
    Used to be cast_unicode, add this temporarily to make sure no further breakage.
    """
    if not isinstance(obj, str):
        raise AssertionError
    return obj

