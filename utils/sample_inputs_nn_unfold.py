
def sample_inputs_nn_unfold(op_info, device, dtype, requires_grad, **kwargs):
    shapes = ((0, 1, 5, 5), (2, 3, 5, 5))
    kernel_sizes = (2, (2, 2), (2, 3))
    dilations = (1, 2, (1, 2))
    paddings = (0, 1, (1, 2))
    strides = (1, 2, (1, 2))

    cases = product(shapes, kernel_sizes, dilations, paddings, strides)
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    for shape, kernel_size, dilation, padding, stride in cases:
        tensor = make_arg(shape)
        yield SampleInput(tensor, kernel_size, dilation, padding, stride)

    # With default args
    yield SampleInput(make_arg((1, 1, 5, 5)), (3, 3))

