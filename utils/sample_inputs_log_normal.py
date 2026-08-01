
def sample_inputs_log_normal(op, device, dtype, requires_grad, **kwargs):

    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=False)
    samples = (
        ((M,), 0, 0.25),
        ((S, S), 0.5, 1),
        ((S, S, S), 0, 0.5),
    )
    for shape, mean, std in samples:
        yield SampleInput(make_arg(shape), args=(mean, std))

