import itertools

def sample_inputs_rot90(op_info, device, dtype, requires_grad=False, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    args = itertools.product(range(-5, 6), [(0, 1), (1, 2), (1, -1)])

    yield SampleInput(make_arg((S, S, S)))
    for arg in args:
        yield SampleInput(make_arg((S, S, S)), args=arg)

