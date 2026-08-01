
def sample_inputs_conv2d(op_info, device, dtype, requires_grad, jit_fail_sample=False, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as shapes for input, weight, bias
    # and a dict of values of (stride, padding, groups, dilation)
    cases: tuple = (
        ((1, 3, 4, 4), (3, 3, 3, 3), (3,),
            {'stride': (2, 2), 'padding': 2, 'groups': 1}),
        ((2, 4, 8, 8), (2, 2, 3, 3), (2,),
            {'stride': (3, 2), 'padding': (2, 1), 'groups': 2, 'dilation': (4, 4)}),
        ((1, 4, 5, 5), (1, 4, 2, 3), (1,),
            {'stride': 2, 'padding': 1, 'groups': 1, 'dilation': (2, 3)}),
        ((1, 4, 5, 5), (1, 4, 2, 3), (1,),
            {'stride': 2, 'padding': 1, 'groups': 1, 'dilation': (2, 3)}),
        ((1, 2, 4, 3), (4, 2, 3, 4), None,
            {'stride': 2, 'padding': 1, 'groups': 1}),
        ((1, 4, 5, 5), (1, 4, 2, 3), (1,),
            {'stride': 2, 'padding': "valid"}),
        ((1, 4, 5, 5), (1, 4, 2, 3), (1,),
            {'stride': 1, 'padding': "same", 'dilation': 3}),
        # Below are the group related samples from common_nn.py
        ((2, 4, 6, 6), (4, 1, 3, 3), (4,), {'groups': 4}),
        ((2, 4, 6, 6), (8, 1, 3, 3), (8,), {'groups': 4}),
        ((2, 4, 6, 6), (8, 1, 3, 3), None, {'groups': 4}),
        ((2, 4, 6, 6), (4, 1, 3, 3), (4,), {'groups': 4, 'stride': (3, 2)}),
        ((2, 4, 6, 6), (4, 1, 3, 3), (4,), {'groups': 4, 'padding': (1, 1)}),
        ((2, 4, 5, 5), (4, 1, 2, 2), (4,), {'groups': 4, 'dilation': (2, 2)}),
        ((2, 4, 6, 5), (6, 2, 3, 2), (6,), {'groups': 2}),
        # With defaults
        ((1, 4, 5, 5), (3, 4, 3, 3), None, {}),
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

