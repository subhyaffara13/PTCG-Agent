
def sample_inputs_geometric(op, device, dtype, requires_grad, **kwargs):

    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=False)
    samples = (
        ((M,), 0.2),
        ((S, S), 0.5),
        ((S, S, S), 0.8),
    )
    for shape, rate in samples:
        yield SampleInput(make_arg(shape), args=(rate,))

