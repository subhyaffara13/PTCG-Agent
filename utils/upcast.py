import functools

def upcast(func):
    """NumPy fft casts inputs to 64 bit and *returns 64-bit results*."""

    @functools.wraps(func)
    def wrapped(tensor, *args, **kwds):
        target_dtype = (
            _dtypes_impl.default_dtypes().complex_dtype
            if tensor.is_complex()
            else _dtypes_impl.default_dtypes().float_dtype
        )
        tensor = _util.cast_if_needed(tensor, target_dtype)
        return func(tensor, *args, **kwds)

    return wrapped


def upcast(*args):
    """Returns the nearest supported sparse dtype for the
    combination of one or more types.

    upcast(t0, t1, ..., tn) -> T  where T is a supported dtype

    Examples
    --------
    >>> from scipy.sparse._sputils import upcast
    >>> upcast('int32')
    <class 'numpy.int32'>
    >>> upcast('bool')
    <class 'numpy.bool'>
    >>> upcast('int32','float32')
    <class 'numpy.float64'>
    >>> upcast('bool',complex,float)
    <class 'numpy.complex128'>

    """

    t = _upcast_memo.get(hash(args))
    if t is not None:
        return t

    upcast = np.result_type(*args)

    for t in supported_dtypes:
        if np.can_cast(upcast, t):
            _upcast_memo[hash(args)] = t
            return t

    raise TypeError(f'no supported conversion for types: {args!r}')

