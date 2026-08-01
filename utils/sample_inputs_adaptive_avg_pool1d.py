
def sample_inputs_adaptive_avg_pool1d(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as (input shape, output size)
    cases = (
        ((0, 8, 8), (5,)),
        ((3, 8, 8), 5),
        ((3, 8, 8), 1)
    )

    for input_shape, output_size in cases:
        # Batched
        yield SampleInput(make_arg(input_shape), args=(output_size,))
        # Unbatched
        yield SampleInput(make_arg(input_shape[1:]), args=(output_size,))

