
def get_expected_stringlength(dtype):
    """Returns the string length when casting the basic dtypes to strings.
    """
    if dtype == np.bool:
        return 5
    if dtype.kind in "iu":
        if dtype.itemsize == 1:
            length = 3
        elif dtype.itemsize == 2:
            length = 5
        elif dtype.itemsize == 4:
            length = 10
        elif dtype.itemsize == 8:
            length = 20
        else:
            raise AssertionError(f"did not find expected length for {dtype}")

        if dtype.kind == "i":
            length += 1  # adds one character for the sign

        return length

    # Note: Can't do dtype comparison for longdouble on windows
    if dtype.char == "g":
        return 48
    elif dtype.char == "G":
        return 48 * 2
    elif dtype.kind == "f":
        return 32  # also for half apparently.
    elif dtype.kind == "c":
        return 32 * 2

    raise AssertionError(f"did not find expected length for {dtype}")

