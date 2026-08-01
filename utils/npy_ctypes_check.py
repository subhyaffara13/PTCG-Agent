
def npy_ctypes_check(cls):
    # determine if a class comes from ctypes, in order to work around
    # a bug in the buffer protocol for those objects, bpo-10746
    try:
        # ctypes class are new-style, so have an __mro__. This probably fails
        # for ctypes classes with multiple inheritance.
        # # (..., _ctypes._CData, object)
        ctype_base = cls.__mro__[-2]
        # right now, they're part of the _ctypes module
        return '_ctypes' in ctype_base.__module__
    except Exception:
        return False

