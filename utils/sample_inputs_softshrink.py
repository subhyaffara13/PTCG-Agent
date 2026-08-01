
def sample_inputs_softshrink(op_info, device, dtype, requires_grad=False, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # The additional sample is to check additional values of lambd beyond the default
    # value (what is already checked by sample_inputs_elementwise_unary)
    for lbda in (0., 0.5):
        yield SampleInput(make_arg(S, S), kwargs={"lambd": lbda})

    yield from sample_inputs_elementwise_unary(op_info, device, dtype, requires_grad)

