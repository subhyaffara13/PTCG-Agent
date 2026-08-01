
def sample_inputs_normal(op, device, dtype, requires_grad, **kwargs):

    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=False)
    samples = (
        ((S, S), 0, 5),
        ((S, S, S), -2, 0.5),
    )
    for shape, mean, std in samples:
        yield SampleInput(make_arg(shape), args=(mean, std))

