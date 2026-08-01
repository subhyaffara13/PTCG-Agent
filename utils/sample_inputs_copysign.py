
def sample_inputs_copysign(op_info, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_elementwise_binary(op_info, device, dtype, requires_grad, **kwargs)
    if dtype.is_floating_point:
        yield SampleInput(make_tensor(5, dtype=dtype, device=device, requires_grad=requires_grad), -3.14)

