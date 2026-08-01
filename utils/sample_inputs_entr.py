
def sample_inputs_entr(op_info, device, dtype, requires_grad, **kwargs):
    low, _ = op_info.domain

    if requires_grad:
        low = 0 + op_info._domain_eps

    make_arg = partial(
        make_tensor, dtype=dtype, device=device, low=low, requires_grad=requires_grad
    )
    yield SampleInput(make_arg((L,)))
    yield SampleInput(make_arg(()))

