
def sample_inputs_exponential(op, device, dtype, requires_grad, **kwargs):

    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=False)
    samples = (
        ((M,), 0.5),
        ((S, S), 1),
        ((S, S, S), 1.5),
    )
    for shape, rate in samples:
        yield SampleInput(make_arg(shape), args=(rate,))

