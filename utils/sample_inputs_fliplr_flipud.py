
def sample_inputs_fliplr_flipud(op_info, device, dtype, requires_grad, **kwargs):
    shapes = [
        (S, M, S),
        (S, 0, M),
    ]
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    return (SampleInput(make_arg(shape, low=None, high=None)) for shape in shapes)

