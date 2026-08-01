
def sample_inputs_channel_shuffle(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    shapes_groups = [
        ((1, 4, 10, 10), 2),
        ((2, 6, 8, 8), 3),
        ((2, 8, 5, 5), 4),
    ]

    yield from (
        SampleInput(make_arg(shape), args=(groups,))
        for shape, groups in shapes_groups
    )

