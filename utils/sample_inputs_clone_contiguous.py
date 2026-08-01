
def sample_inputs_clone_contiguous(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    yield SampleInput(make_arg((S, M, S)))
    yield SampleInput(make_arg(()))

