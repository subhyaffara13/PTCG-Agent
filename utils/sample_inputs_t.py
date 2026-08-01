
def sample_inputs_t(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    yield SampleInput(make_arg((1, 2)))
    yield SampleInput(make_arg((2,)))
    yield SampleInput(make_arg(()))


def sample_inputs_T(self, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    shapes = ((M, M), (M, L))
    return (SampleInput(make_arg(shape)) for shape in shapes)

