
def sample_inputs_logit(op_info, device, dtype, requires_grad, **kwargs):
    low, high = op_info.domain

    # Note: Operator is very sensitive at points near the
    # start and end of domain and leads to NaN for float16
    # if domain_eps is 1e-5.
    if dtype.is_floating_point or dtype.is_complex:
        domain_eps = op_info._domain_eps if dtype != torch.float16 else 3e-2

        low = low + domain_eps
        high = high - domain_eps

    make_arg = partial(make_tensor, dtype=dtype, device=device, low=low, high=high, requires_grad=requires_grad)

    yield SampleInput(make_arg((S, S, S)))
    yield SampleInput(make_arg((S, S, S)), 0.2)
    yield SampleInput(make_arg(()))
    yield SampleInput(make_arg(()), 0.2)

