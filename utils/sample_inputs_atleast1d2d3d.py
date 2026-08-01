
def sample_inputs_atleast1d2d3d(op_info, device, dtype, requires_grad, **kwargs):
    shapes = ((S, S, S, S), (S, S, S), (S, S), (S, ), (),)
    make_tensor_partial = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    for shape in shapes:
        yield SampleInput(make_tensor_partial(shape))
    yield SampleInput([make_tensor_partial(shape) for shape in shapes])

