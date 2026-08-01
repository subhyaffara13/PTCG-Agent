
def sample_inputs_conv_transpose3d(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as shapes for input, weight, bias
    # and a dict of values of (stride, padding, output_padding, groups, dilation)
    cases: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], dict] = (
        ((1, 3, 4, 4, 4), (3, 3, 3, 3, 3), (3,),
         {'stride': (2, 2, 2), 'padding': 2, 'output_padding': (1, 1, 1), 'groups': 1}),
        ((2, 2, 4, 4, 4), (2, 2, 4, 5, 6), (4,),
         {'stride': (3, 2, 1), 'padding': (1, 2, 3), 'output_padding': (2, 3, 1), 'groups': 2, 'dilation': (4, 4, 4)}),
        ((1, 1, 4, 5, 2), (1, 1, 4, 3, 1), (1,),
         {'stride': 2, 'padding': 1, 'output_padding': 1, 'groups': 1, 'dilation': (2, 3, 2)}),
        ((1, 1, 4, 3, 4), (1, 2, 3, 4, 5), None,
         {'stride': 2, 'padding': 1, 'output_padding': 1, 'groups': 1}),
        ((1, 4, 5, 5, 5), (4, 8, 3, 3, 3), None,
         {})
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

