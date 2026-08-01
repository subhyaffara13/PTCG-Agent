
def sample_inputs_matrix_exp(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    yield SampleInput(make_arg((S, S)))
    yield SampleInput(make_arg((S, S, S)))

