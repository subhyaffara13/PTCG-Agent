
def sample_inputs_fill(op_info, device, dtype, requires_grad, **kwargs):
    # scalar case
    unary_func = partial(sample_inputs_elementwise_njt_unary, op_kwargs={"value": 42.0})
    yield from unary_func(op_info, device, dtype, requires_grad)

