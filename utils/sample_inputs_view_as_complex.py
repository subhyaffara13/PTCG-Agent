
def sample_inputs_view_as_complex(op_info, device, dtype, requires_grad, **kwargs):
    yield SampleInput(make_tensor((S, 2), dtype=dtype, device=device, requires_grad=requires_grad))

