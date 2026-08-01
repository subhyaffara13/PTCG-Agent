
def sample_inputs_conv3d(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as shapes for input, weight, bias
    # and dict of values of (stride, padding, dilation, groups)
    cases: tuple = (
        ((1, 1, 4, 4, 4), (1, 1, 1, 1, 1), (1,), {'padding': 'same'}),
        ((1, 1, 4, 4, 4), (1, 1, 4, 4, 4), (1,), {'stride': (2, 2, 2)}),
        ((1, 1, 5, 5, 5), (1, 1, 3, 3, 3), (1,), {'dilation': 2}),
        ((1, 1, 1, 1, 10), (1, 1, 1, 1, 4), None, {'padding': 'valid'}),
        ((1, 1, 10, 11, 12), (1, 1, 1, 2, 5), None, {'padding': 'same'}),
        ((1, 1, 10, 11, 12), (1, 1, 1, 2, 5), None, {'padding': 'same', 'dilation': 2}),
        ((1, 1, 10, 11, 12), (1, 1, 4, 4, 4), None, {'padding': 'same', 'dilation': 3}),
        ((1, 1, 1, 1, 10), (1, 1, 1, 1, 4), None, {'padding': 'valid'}),
        ((3, 9, 3, 1, 9), (3, 3, 3, 1, 9), (3,), {'groups': 3}),
        ((3, 9, 3, 1, 9), (3, 3, 3, 1, 9), (3,), {'stride': (2, 2, 2), 'dilation': 1, 'groups': 3}),
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

