
def use_arraytype(arraytype):
    """pygame.sndarray.use_arraytype(arraytype): return None

    DEPRECATED - only numpy arrays are now supported.
    """
    warnings.warn(
        DeprecationWarning(
            "only numpy arrays are now supported, "
            "this function will be removed in a "
            "future version of the module"
        )
    )
    arraytype = arraytype.lower()
    if arraytype != "numpy":
        raise ValueError("invalid array type")


def use_arraytype(arraytype):
    """pygame.surfarray.use_arraytype(arraytype): return None

    DEPRECATED - only numpy arrays are now supported.
    """
    warnings.warn(
        DeprecationWarning(
            "only numpy arrays are now supported, "
            "this function will be removed in a "
            "future version of the module"
        )
    )
    arraytype = arraytype.lower()
    if arraytype != "numpy":
        raise ValueError("invalid array type")

