
def sample_inputs_multi_margin_loss(op_info, device, dtype, requires_grad, **kwargs):
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_target = partial(_make_tensor, dtype=torch.long, requires_grad=False)
    make_weight = partial(_make_tensor, requires_grad=False)

    inputs = (
        ((), make_target([], low=0, high=1), {}),
        ((S,), make_target([], low=0, high=S), {"p": 1}),
        ((S,), make_target([1], low=0, high=S), {"p": 2}),
        ((S, M), make_target([S], low=0, high=M), {"margin": 1.0}),
        ((S, M), make_target([S], low=0, high=M), {"margin": -3.14}),
        ((M, S), make_target([M], low=0, high=S), {"weight": None}),
        ((M, S), make_target([M], low=0, high=S), {"weight": make_weight([S], low=-10., high=10.)}),
        ((M, S), make_target([M], low=0, high=S), {"reduction": "none"}),
        ((M, S), make_target([M], low=0, high=S), {"reduction": "mean"}),
        ((M, S), make_target([M], low=0, high=S), {"reduction": "sum"}),
    )

    for input_shape, target, kwargs in inputs:
        yield SampleInput(_make_tensor(input_shape), args=(target,), kwargs=kwargs)

