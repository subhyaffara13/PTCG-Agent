
def sample_inputs_conv1d(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as shapes for input, weight, bias,
    # and a dict of values of (stride, padding, dilation, groups)
    cases: tuple = (
        ((1, 3, 4), (3, 3, 3), (3,), {'stride': (2,), 'padding': 2, 'groups': 1}),
        ((2, 4, 8), (2, 2, 3), (2,), {'stride': 3, 'padding': 1, 'groups': 2, 'dilation': 2}),
        ((1, 4, 5), (1, 4, 3), None, {'stride': (2,), 'padding': 'valid'}),
        ((2, 2, 4), (2, 1, 4), (2,), {'stride': (1,), 'padding': 'same', 'groups': 2, 'dilation': (2,)}),
        # With defaults
        ((1, 4, 5), (3, 4, 3), None, {}),
    )

    for input_shape, weight, bias, kwargs in cases:
        # Batched
        yield SampleInput(make_arg(input_shape), args=(
            make_arg(weight),
            make_arg(bias) if bias is not None else bias
        ), kwargs=kwargs)
        # Unbatched
        yield SampleInput(make_arg(input_shape[1:]), args=(
            make_arg(weight),
            make_arg(bias) if bias is not None else bias
        ), kwargs=kwargs)

