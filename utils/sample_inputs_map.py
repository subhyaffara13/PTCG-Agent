
def sample_inputs_map(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = functools.partial(
        make_tensor, device=device, dtype=dtype, requires_grad=requires_grad
    )
    yield SampleInput(
        [make_arg(2, 2, 2, low=0.1, high=2), make_arg(2, 2, 2, low=0.1, high=2)],
        args=(make_arg(1, low=0.1, high=2), make_arg(1, low=0.1, high=2)),
    )

