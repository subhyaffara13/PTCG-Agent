
def sample_inputs_sum_to_size(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    # list of tuples (shape, shape) defining the shapes of the input and output tensors
    sample_shapes = [
        ((), ()),
        ((S,), (1,)),
        ((S, S), (1, 1)),
        ((S, S), (1, S)),
        ((S, S), (S, S)),
        ((S, S, S), (S, 1, S)),
    ]

    for input_shape, output_shape in sample_shapes:
        yield SampleInput(make_arg(input_shape), args=(output_shape,))
        if output_shape == ():
            continue
        yield SampleInput(make_arg(input_shape), args=(list(output_shape),))
        yield SampleInput(make_arg(input_shape), args=(*output_shape,))

