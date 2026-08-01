
def sample_inputs_flatten(op_info, device, dtype, requires_grad, **kwargs):
    shapes = ((S, S, S), (S, S), (S, ), (),)
    make_tensor_partial = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    for shape in shapes:
        yield SampleInput(make_tensor_partial(shape))
        if len(shape) > 1:
            yield SampleInput(make_tensor_partial(shape), start_dim=1, end_dim=-1)

