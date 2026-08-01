
def sample_inputs_cartesian_prod(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(torch.tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # constructs 1-D tensors with varying number of elements
    a = make_arg((0,))
    b = make_arg((0, 1))
    c = make_arg((0, 1, 2, 3))

    # sample with only 1 tensor
    yield SampleInput(a)

    # sample with 2 tensors
    yield SampleInput(a, b)

    # sample with 3 tensors
    yield SampleInput(a, b, c)

