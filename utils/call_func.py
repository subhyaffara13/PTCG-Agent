
def call_func(func, args, array, sanitize=True):
    if args == (None, None):
        return func(array, array)
    if args[0] is None:
        if sanitize:
            san_args = tuple(
                np.array(arg, dtype=array.dtype) if isinstance(arg, str) else
                arg for arg in args[1:]
            )
        else:
            san_args = args[1:]
        return func(array, *san_args)
    if args[1] is None:
        return func(args[0], array)
    # shouldn't ever happen
    assert 0

