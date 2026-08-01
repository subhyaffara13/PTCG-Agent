
def sample_inputs_alias_copy(op_info, device, dtype, requires_grad, **kwargs):
    yield SampleInput(make_tensor((S,), dtype=dtype, device=device, requires_grad=requires_grad))
    yield SampleInput(make_tensor((), dtype=dtype, device=device, requires_grad=requires_grad))

