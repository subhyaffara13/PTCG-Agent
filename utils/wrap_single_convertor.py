import functools

def wrap_single_convertor(convert_single):
    """
    Wraps a ``__ua_convert__`` defined for a single element to all elements.
    If any of them return ``NotImplemented``, the operation is assumed to be
    undefined.

    Accepts a signature of (value, type, coerce).
    """

    @functools.wraps(convert_single)
    def __ua_convert__(dispatchables, coerce):
        converted = []
        for d in dispatchables:
            c = convert_single(d.value, d.type, coerce and d.coercible)

            if c is NotImplemented:
                return NotImplemented

            converted.append(c)

        return converted

    return __ua_convert__

