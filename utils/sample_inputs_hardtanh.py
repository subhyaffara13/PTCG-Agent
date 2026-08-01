
def sample_inputs_hardtanh(op_info, device, dtype, requires_grad=False, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # The additional sample is to check additional values of min_val and max_val beyond the default
    # value (what is already checked by sample_inputs_elementwise_unary)
    for max_val, min_val in ((0.5, -0.5), (0., 0.)):
        yield SampleInput(make_arg(S, S), kwargs={"min_val": min_val, "max_val": max_val})

    yield from sample_inputs_elementwise_unary(op_info, device, dtype, requires_grad)

