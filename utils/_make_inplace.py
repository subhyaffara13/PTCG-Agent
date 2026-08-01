
def _make_inplace(fn):
    """
    Given a function with out variant (i.e. using `out_wrapper()), it returns its in-place variant
    See https://github.com/pytorch/pytorch/wiki/Developer-FAQ#how-do-in-place-operations-work-in-pytorch
    """

    # nb. We use the name of the first argument used in the unary references
    @wraps(fn)
    def _fn(a, *args, **kwargs):
        return fn(a, *args, out=a, **kwargs)

    inplace_name = f"{fn.__name__}_"
    _fn.__name__ = inplace_name
    _fn = register_decomposition(getattr(aten, inplace_name))(_fn)  # type: ignore[assignment]

    # We access the __all__ attribute of the module where fn is defined
    # There may be a cleaner way of doing this...
    from inspect import getmodule

    _all = getmodule(fn).__all__  # type: ignore[union-attr]
    if inplace_name not in _all:
        _all.append(inplace_name)
    return _fn

