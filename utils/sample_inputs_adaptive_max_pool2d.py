
def sample_inputs_adaptive_max_pool2d(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as (input shape, output size)
    cases = (
        # ((0, 8, 8, 8), (5, 7)),
        # 0 batch size doesn't work,  cannot reshape tensor of 0 elements into shape [0, 8, -1]
        ((1, 4, 4, 4), (2, 3)),
        ((2, 4, 4, 4), (None, 3)),
        ((2, 4, 4, 4), (1, 1)),
        ((1, 4, 4, 3), (3, None)),
        ((1, 4, 4, 3), (None, None)),
        ((1, 4, 4, 3), (3)),
    )

    for shapes, return_idx in product(cases, (True, False)):
        # Batched
        yield SampleInput(make_arg(shapes[0]), args=(shapes[1], return_idx))
        # Unbatched
        yield SampleInput(make_arg(shapes[0][1:]), args=(shapes[1], return_idx))

