
def sample_inputs_ravel(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device,
                       low=None, high=None, requires_grad=requires_grad)
    yield SampleInput(make_arg((S, S, S)))
    yield SampleInput(make_arg(()))
    yield SampleInput(make_arg((S, S, S), noncontiguous=True))

