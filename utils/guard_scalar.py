
def guard_scalar(
    a: SymBool | SymInt | SymFloat | int | bool | float,
) -> bool | int | float:
    """
    Guard a scalar value, which can be a symbolic or concrete boolean, integer, or float.

    This function dispatches to the appropriate guard function based on the type of the input.

    Args:
        a: A symbolic or concrete scalar value (bool, int, or float)

    Returns:
        The concrete value after guarding

    Raises:
        AssertionError: If the input is not a recognized scalar type
    """
    if isinstance(a, (SymBool, bool)):
        return guard_bool(a)
    elif isinstance(a, (SymInt, int)):
        return guard_int(a)
    elif isinstance(a, (SymFloat, float)):
        return guard_float(a)
    else:
        raise AssertionError(f"unrecognized scalar {a}")

