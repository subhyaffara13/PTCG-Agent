
def sample_inputs_logaddexp(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    shape = (S, S)
    yield SampleInput(make_arg(shape), make_arg(shape))

