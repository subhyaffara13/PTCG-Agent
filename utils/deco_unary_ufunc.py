
def deco_unary_ufunc(torch_func):
    """Common infra for unary ufuncs.

    Normalize arguments, sort out type casting, broadcasting and delegate to
    the pytorch functions for the actual work.
    """

    @normalizer
    def wrapped(
        x: ArrayLike,
        /,
        out: OutArray | None = None,
        *,
        where=True,
        casting: CastingModes | None = "same_kind",
        order="K",
        dtype: DTypeLike | None = None,
        subok: NotImplementedType = False,
        signature=None,
        extobj=None,
    ):
        if dtype is not None:
            x = _util.typecast_tensor(x, dtype, casting)

        if torch_func.__name__ in _fp_unary:
            x = _util.cast_int_to_float(x)

        result = torch_func(x)
        result = _ufunc_postprocess(result, out, casting)
        return result

    wrapped.__qualname__ = torch_func.__name__
    wrapped.__name__ = torch_func.__name__

    return wrapped

