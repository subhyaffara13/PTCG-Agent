
def sample_inputs_max_min_reduction_no_dim(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad, low=None, high=None)
    yield SampleInput(make_arg((S, S, S)))
    yield SampleInput(make_arg(()))

