
def sample_inputs_roll(op_info, device, dtype, requires_grad=False, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    args = ((0, 0), (1, 2), (0, 2), (2, 0), (-1, 0), (10000, 1), (2,), ((1, 2, -1), (0, 1, 2)))

    for arg in args:
        yield SampleInput(make_arg((0, 0, 0)), args=arg)
        yield SampleInput(make_arg((S, S, S)), args=arg)

    # Scalar tensor
    yield SampleInput(make_arg(()), args=(10, ))

