
def reference_inputs_flatten(op, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_flatten(op, device, dtype, requires_grad, **kwargs)

    # shape x start_dim x end_dim
    cases = (
        ((5, 4, 0, 1, 3, 7), 1, 3),
        ((5, 4, 0, 1, 3, 7), 4, 5),
        ((5, 4, 1, 1, 3, 7), 2, 3),
        ((), 0, -1),
        ((1,), 0, -1),
        ((3, 7, 5), 1, 2),
        ((4, 5), 1, 1),
        ((1, 5, 5, 1, 5, 1, 5, 1), 0, 2),
        ((1, 5, 5, 1, 5, 1, 5, 1), 3, -1),
        ((1, 5, 5, 1, 5, 7, 5, 1), -2, -1),
        ((2, 4, 2), 0, 1),
        ((4, 2, 2), 1, 2),
        ((0, 3, 4, 5), 1, 3),
    )

    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    for shape, start, end in cases:
        yield SampleInput(make_arg(shape), args=(start, end,))
        yield SampleInput(make_arg(shape, noncontiguous=True).transpose(0, -1), args=(start, end,))
        yield SampleInput(make_arg(shape).transpose(0, -1), args=(start, end,))

