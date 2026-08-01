
def reference_movedim_moveaxis(op_info, device, dtype, requires_grad, **kwargs):
    yield from sample_movedim_moveaxis(op_info, device, dtype, requires_grad, **kwargs)

    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # shape, source, destination
    args = (
        # empty inputs
        ((), (), ()),
        # int inputs, negative
        ((3, 5, 7, 2), -2, 1),
        # swap bounds
        ((3, 5, 7, 2), (-1, 0), (0, -1)),
        # non-sequential, negative
        ((2, 3, 4, 5, 6), (3, -3, 4), (1, 0, -1)),
        # idempotence, negative
        ((2, 3, 4, 5, 6), (-3, 4, 3, 1), (-3, 4, 3, 1)),
        # reverse, sequential, positive
        ((6, 2, 3, 5, 4), (4, 3, 2, 1, 0), (0, 1, 2, 3, 4)),
        # reverse, non-sequential
        ((6, 2, 3, 5, 4), (-3, -2, -4, -5, -1), (2, 1, 3, 4, 0)),
        # reverse, sequential, negative
        ((6, 2, 3, 5, 4), (4, -2, 2, -4, -5), (-5, 1, 2, -2, -1)),
    )

    for shape, source, destination in args:
        yield SampleInput(make_arg(shape), args=(source, destination))

