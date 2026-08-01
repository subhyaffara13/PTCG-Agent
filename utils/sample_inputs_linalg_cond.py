
def sample_inputs_linalg_cond(op_info, device, dtype, requires_grad=False, **kwargs):
    make_arg = partial(
        make_tensor, dtype=dtype, device=device, requires_grad=requires_grad
    )

    # autograd is not supported for inputs with zero number of elements
    shapes = (
        (S, S),
        (2, S, S),
        (2, 1, S, S),
    )

    for shape in shapes:
        yield SampleInput(make_arg(shape))

