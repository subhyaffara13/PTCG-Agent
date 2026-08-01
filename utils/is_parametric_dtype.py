
def is_parametric_dtype(dtype):
    """Returns True if the dtype is a parametric legacy dtype (itemsize
    is 0, or a datetime without units)
    """
    if dtype.itemsize == 0:
        return True
    if issubclass(dtype.type, (np.datetime64, np.timedelta64)):
        if dtype.name.endswith("64"):
            # Generic time units
            return True
    return False

