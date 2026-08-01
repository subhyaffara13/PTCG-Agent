
def sample_inputs_prelu(op_info, device, dtype, requires_grad, **kwargs):
    op_kwargs = op_info.sample_kwargs(device, dtype, None)[0]
    yield from sample_inputs_elementwise_unary(op_info, device, dtype, requires_grad,
                                               op_kwargs=op_kwargs)

    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    cases = (
        (()),
        ((S, )),
        ((S, S)),
        ((S, M, S))
    )

    for shape in cases:
        for weight in [-1., 0., 0.8, 1.]:
            weight_tensor = torch.tensor(weight, device=device, dtype=dtype, requires_grad=requires_grad)
            yield SampleInput(make_arg(shape), args=(weight_tensor,))

        channel_size = shape[1] if len(shape) >= 2 else 1
        yield SampleInput(make_arg(shape), args=(make_arg((channel_size,)),))

    weight_tensor = torch.tensor(1., device=device, dtype=dtype, requires_grad=requires_grad)

    yield SampleInput(make_arg((S, S)), kwargs=dict(weight=weight_tensor,))
    yield SampleInput(make_arg((S, S)), kwargs=dict(weight=make_arg((S,)),))

