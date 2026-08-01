
def sample_inputs_diagflat(op_info, device, dtype, requires_grad, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    yield SampleInput(make_input(()))
    yield SampleInput(make_input((2,)))
    yield SampleInput(make_input((2, 2)))
    yield SampleInput(make_input((2,)), offset=1)
    yield SampleInput(make_input((2,)), offset=-1)

