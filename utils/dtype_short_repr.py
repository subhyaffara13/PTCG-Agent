
def dtype_short_repr(dtype):
    """
    Convert a dtype to a short form which evaluates to the same dtype.

    The intent is roughly that the following holds

    >>> from numpy import *
    >>> dt = np.int64([1, 2]).dtype
    >>> assert eval(dtype_short_repr(dt)) == dt
    """
    if not type(dtype)._legacy:
        # TODO: Custom repr for user DTypes, logic should likely move.
        return repr(dtype)
    if dtype.names is not None:
        # structured dtypes give a list or tuple repr
        return str(dtype)
    elif issubclass(dtype.type, flexible):
        # handle these separately so they don't give garbage like str256
        return f"'{str(dtype)}'"

    typename = dtype.name
    if not dtype.isnative:
        # deal with cases like dtype('<u2') that are identical to an
        # established dtype (in this case uint16)
        # except that they have a different endianness.
        return f"'{str(dtype)}'"
    # quote typenames which can't be represented as python variable names
    if typename and not (typename[0].isalpha() and typename.isalnum()):
        typename = repr(typename)
    return typename

