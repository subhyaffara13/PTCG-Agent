
def sample_inputs_binary_cross_entropy_with_logits(
    op_info, device, dtype, requires_grad, **kwargs
):
    make = partial(make_tensor, device=device, dtype=dtype)
    make_prob = partial(make, low=0, high=1)
    reductions = ("mean", "sum", "none")

    def make_weight_shape_kwargs():
        kwargs = []
        for shape in ((1,), (1, S), (S), (S, S)):
            kwargs.extend([((S, S), dict(reduction=reduction, weight=make(shape))) for reduction in reductions])
        return kwargs

    shapes_and_kwargs = [
        *[(shape, None) for shape in ((), (1,), (S,), (S, S), (S, S, S))],
        *[((S, S), dict(reduction=reduction)) for reduction in reductions],
        *make_weight_shape_kwargs(),
        *[((S, S), dict(reduction=reduction, pos_weight=make((S,), low=0))) for reduction in reductions],
        *[((S, S), dict(reduction=reduction, weight=make((S, S)), pos_weight=make((S,), low=0))) for reduction in reductions],
    ]

    for shape, kwargs in shapes_and_kwargs:
        yield SampleInput(
            make(shape, requires_grad=requires_grad),
            args=(make_prob(shape, requires_grad=requires_grad),),
            kwargs=kwargs,
        )

