
def sample_inputs_multilabel_margin_loss(op_info, device, dtype, requires_grad, **kwargs):
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_target = partial(_make_tensor, dtype=torch.long, requires_grad=False)

    inputs = (
        ([], make_target([], low=0, high=1), {}),
        ([S], make_target([S], low=0, high=S), {}),
        ([M, S], make_target([M, S], low=0, high=S), {}),
        ([M, S], make_target([M, S], low=0, high=S), {"reduction": "none"}),
        ([M, S], make_target([M, S], low=0, high=S), {"reduction": "mean"}),
        ([M, S], make_target([M, S], low=0, high=S), {"reduction": "sum"}),
    )

    for shape, target, kwargs in inputs:
        yield SampleInput(_make_tensor(shape), args=(target,), kwargs=kwargs)

