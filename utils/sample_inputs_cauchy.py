
def sample_inputs_cauchy(op, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=False)
    samples = (
        ((M,), 0, 0.5),
        ((S, S), 0, 1),
        ((S, S, S), -2, 1),
    )
    for shape, median, gamma in samples:
        yield SampleInput(make_arg(shape), args=(median, gamma))

