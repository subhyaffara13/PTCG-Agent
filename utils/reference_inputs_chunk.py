
def reference_inputs_chunk(op, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_chunk(op, device, dtype, requires_grad, **kwargs)

    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    # shape x chunks x dim
    cases = (
        ((13, 9, 11), 17, -1),
        ((13, 9, 11), 11, -1),
        ((13,), 12, -1),
        ((15,), 12, -1),
        ((15,), 7, 0),
        ((15,), 9, 0),
        ((3, 7), 9, 1),
        ((3, 7), 9, 0),
        ((3, 7), 2, 0),
        ((3, 7), 3, 0),
        ((3, 7), 1, 0),
        ((3, 7), 1, 1),
        ((4, 4), 2, 0),
    )

    for shape, chunks, dim in cases:
        yield SampleInput(make_arg(shape), args=(chunks, dim))

