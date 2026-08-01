
def register_foreach_pointwise(
    aten_fn,
    pointwise_lowering_fn,
    allow_alpha=False,
    scalar_kwarg="alpha",
):
    fn = make_foreach_pointwise(
        pointwise_lowering_fn, allow_alpha=allow_alpha, scalar_kwarg=scalar_kwarg
    )
    fn = _register_foreach_lowering(aten_fn, fn)
    return fn

