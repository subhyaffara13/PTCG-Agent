
def sample_inputs_slice(op_info, device, dtype, requires_grad, **kwargs):

    make_input = partial(make_tensor, device=device, dtype=dtype,
                         low=None, high=None, requires_grad=requires_grad)

    yield SampleInput(make_input(3), 0)

    yield SampleInput(make_input(20, 30, 40), dim=1, start=1, end=-2)

    yield SampleInput(make_input(20, 30, 40), dim=1, start=1, end=-2, step=3)

    yield SampleInput(make_input(20, 30, 40), dim=0, start=-10, end=-2, step=2)

