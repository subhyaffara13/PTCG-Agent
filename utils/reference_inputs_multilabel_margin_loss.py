
def reference_inputs_multilabel_margin_loss(op_info, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_multilabel_margin_loss(op_info, device, dtype, requires_grad, **kwargs)
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_target = partial(_make_tensor, dtype=torch.long, requires_grad=False)
    make_target_tensor = partial(torch.tensor, device=device, dtype=torch.long, requires_grad=False)

    inputs = (
        # random tests including -1 target labels
        ([], make_target([], low=-1, high=1)),
        ([S], make_target([S], low=-1, high=S)),
        ([M, S], make_target([M, S], low=-1, high=S)),
        # repeated target labels and -1 (labels after the first -1 are ignored)
        ([], make_target_tensor(-1)),
        ([7], make_target_tensor([2, 0, 6, -1, 4, -1, 6])),
        ([4, 5], make_target_tensor([[4, -1, 0, -1, 2], [0, 0, 4, 1, 4], [-1, 3, -1, 1, 0], [4, 3, 2, 1, 0]])),
    )
    reductions = (None, "none", "mean", "sum")

    for (shape, target), reduction in product(inputs, reductions):
        kwargs = {}
        if reduction is not None:
            kwargs["reduction"] = reduction
        yield SampleInput(_make_tensor(shape), args=(target,), kwargs=kwargs)

