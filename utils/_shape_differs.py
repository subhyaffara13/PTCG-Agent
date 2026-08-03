import sys

def _shape_differs(t1: type[object], t2: type[object]) -> bool:
    """Check whether two types differ in shape.

    Mirrors the shape_differs() function in typeobject.c in CPython."""
    if sys.version_info >= (3, 12):
        return t1.__basicsize__ != t2.__basicsize__ or t1.__itemsize__ != t2.__itemsize__
    else:
        # CPython had more complicated logic before 3.12:
        # https://github.com/python/cpython/blob/f3c6f882cddc8dc30320d2e73edf019e201394fc/Objects/typeobject.c#L2224
        # We attempt to mirror it here well enough to support the most common cases.
        if t1.__itemsize__ or t2.__itemsize__:
            return t1.__basicsize__ != t2.__basicsize__ or t1.__itemsize__ != t2.__itemsize__
        t_size = t1.__basicsize__
        if not t2.__weakrefoffset__ and t1.__weakrefoffset__ + SIZEOF_PYOBJECT == t_size:
            t_size -= SIZEOF_PYOBJECT
        if not t2.__dictoffset__ and t1.__dictoffset__ + SIZEOF_PYOBJECT == t_size:
            t_size -= SIZEOF_PYOBJECT
        if not t2.__weakrefoffset__ and t2.__weakrefoffset__ == t_size:
            t_size -= SIZEOF_PYOBJECT
        return t_size != t2.__basicsize__

