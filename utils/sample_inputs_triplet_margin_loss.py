
def sample_inputs_triplet_margin_loss(op_info, device, dtype, requires_grad, with_distance=False, **kwargs):
    make = partial(make_tensor, (S, M), device=device, dtype=dtype, requires_grad=requires_grad)

    kwargss = (
        *[dict(margin=margin) for margin in (1e-6, 1.0, 10.0)],
        dict(swap=True),
        *[dict(reduction=reduction) for reduction in ("mean", "sum", "none")],
    )

    for kwargs in kwargss:
        input = make()
        args = (make(), make())
        if with_distance:
            kwargs["distance_function"] = torch.nn.PairwiseDistance()
        yield SampleInput(input, args=args, kwargs=kwargs)

