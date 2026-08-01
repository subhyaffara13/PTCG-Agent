
def _get_ctypes_data(data):
    # Get voidp pointer
    return ctypes.cast(data, ctypes.c_void_p).value


def _get_ctypes_data():
    value = ctypes.c_double(2.0)
    return ctypes.cast(ctypes.pointer(value), ctypes.c_voidp)

