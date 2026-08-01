
def get_arraytype():
    """pygame.sndarray.get_arraytype(): return str

    DEPRECATED - only numpy arrays are now supported.
    """
    warnings.warn(
        DeprecationWarning(
            "only numpy arrays are now supported, "
            "this function will be removed in a "
            "future version of the module"
        )
    )
    return "numpy"


def get_arraytype():
    """pygame.surfarray.get_arraytype(): return str

    DEPRECATED - only numpy arrays are now supported.
    """
    warnings.warn(
        DeprecationWarning(
            "only numpy arrays are now supported, "
            "this function will be removed in a "
            "future version of the module"
        )
    )
    return "numpy"

