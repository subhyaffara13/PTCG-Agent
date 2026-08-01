
def xp_result_device(*args):
    """Return the device of an array in `args`, for the purpose of
    input-output device propagation.
    If there are multiple devices, return an arbitrary one.
    If there are no arrays, return None (this typically happens only on NumPy).
    """
    for arg in args:
        # Do not do a duck-type test for the .device attribute, as many backends today
        # don't have it yet. See workarouunds in array_api_compat.device().
        if is_array_api_obj(arg):
            return xp_device(arg)
    return None

