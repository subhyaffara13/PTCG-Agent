
def sample_inputs_stack(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # shape x number of tensors
    cases = (
        ((3, 4), 1),
        ((1, 2, 1, 4), 3),
        ((0, 1, 0), 2),)

    for shape, num_tensors in cases:
        tensors = [make_arg(shape) for _ in range(num_tensors)]
        for dim in range(-1, len(shape) - 1):
            yield SampleInput(tensors, args=(dim,))

