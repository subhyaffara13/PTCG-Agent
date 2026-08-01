
def _check_type(cond, message=None):  # noqa: F811
    r"""Throws error containing an optional message if the specified condition
    is False.

    Error type: ``TypeError``

    C++ equivalent: ``TORCH_CHECK_TYPE``

    Args:
        cond (:class:`bool`): If False, throw error

        message (Callable, optional): Callable that returns either a string or
            an object that has a ``__str__()`` method to be used as the error
            message. Default: ``None``
    """
    _check_with(TypeError, cond, message)  # pyrefly: ignore [bad-argument-type]


def _check_type(*args, zero_point_index=-1):
    new_args = []
    for i, a in enumerate(args):
        if numpy.issubdtype(type(a), numpy.number):
            new_args.append(numpy.array(a))
        elif isinstance(a, numpy.ndarray):
            new_args.append(a)
        else:
            raise TypeError(f"arg {i} is not an array: {a}")
        if i == zero_point_index:
            v = new_args[-1]
            if v.dtype == numpy.float32 or v.dtype == numpy.float16:
                raise TypeError(f"zero_point cannot be {v.dtype}")
    return tuple(new_args) if len(new_args) > 1 else new_args[0]

