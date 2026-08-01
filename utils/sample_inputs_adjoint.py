
def sample_inputs_adjoint(self, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    shapes = ((1, 2, 3), (M, M), (S, S, S), (S, M, S), (M, S, M, S))
    return (SampleInput(make_arg(shape)) for shape in shapes)

