
def sample_movedim_moveaxis(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, low=None, high=None, requires_grad=requires_grad)
    yield SampleInput(make_arg((4, 3, 2, 1)), [0, 1, 2, 3], [3, 2, 1, 0])
    yield SampleInput(make_arg((4, 3, 2, 1)), [0, -1, -2, -3], [-3, -2, -1, -0])

