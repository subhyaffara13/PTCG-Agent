
def sample_inputs_as_strided_scatter(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # input shape, output shape, output stride, output storage offset
    test_cases = [
        ((1,), (), (), 0),
        ((1,), (1,), (1,), 0),
        ((3, 3), (2, 2), (1, 2), 0),
        ((3, 3), (2, 2), (1, 2), 1),
        ((3, 3), (2, 2), (2, 1), 0),
        # Scatter to larger dimensions
        ((16,), (2, 2, 2, 2), (8, 4, 2, 1), 0),
        # Scatter to larger dimensions with strides inverted
        ((16,), (2, 1, 1, 2), (1, 2, 4, 8), 0),
    ]

    for input_shape, output_shape, stride, storage_offset in test_cases:
        input_t = make_arg(input_shape)
        input_src = make_arg(output_shape)
        yield SampleInput(input_t, input_src, output_shape, stride, storage_offset=storage_offset)

