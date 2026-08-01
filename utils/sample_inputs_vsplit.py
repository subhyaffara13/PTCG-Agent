
def sample_inputs_vsplit(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device,
                       low=None, high=None, requires_grad=requires_grad)
    yield SampleInput(make_arg(6, S), 2)
    yield SampleInput(make_arg(S, S, S), [1, 2, 3])

