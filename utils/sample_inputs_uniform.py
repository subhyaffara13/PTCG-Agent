
def sample_inputs_uniform(op, device, dtype, requires_grad, **kwargs):

    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=False)
    samples = (
        ((M,), -100, 100),
        ((S, S), 0, 1),
        ((S, S, S), 1, 2),
    )
    for shape, hi, lo in samples:
        yield SampleInput(make_arg(shape), args=(hi, lo))

