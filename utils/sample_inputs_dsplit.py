
def sample_inputs_dsplit(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device,
                       low=None, high=None, requires_grad=requires_grad)
    yield SampleInput(make_arg(S, S, S), [1, 2, 3])
    yield SampleInput(make_arg(S, S, 6), 2)

