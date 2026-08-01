
def sample_inputs_nn_pad_replicate_negative(op_info, device, dtype, requires_grad, **kwargs):
    cases: tuple = (
        ((5, 3, 4, 4), (-4, 5, 0, 0)),
        ((6, 2, 4, 4), (0, 0, 2, -4)),
        ((5, 6, 4, 4), (5, -4, -4, 3)),
        ((4, 2, 5, 5), (-2, -1, 4, 6)),
        ((2, 6, 5, 5), (8, -1, -1, -3)),
        ((8, 1, 5, 5), (-2, -1, -1, -3)),
    )
    make_inp = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    for shape, pad in cases:
        yield SampleInput(make_inp(shape), args=(pad, 'replicate'))

