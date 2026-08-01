
def get_clib_test_routine(name, restype, *argtypes):
    ptr = getattr(clib_test, name)
    return ctypes.cast(ptr, ctypes.CFUNCTYPE(restype, *argtypes))

