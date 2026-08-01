
def sample_inputs_nonzero_static(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    sizes = ((), (S,), (S, S), (S, S, S), (S, 1, S), (S, 0, S))

    inputs = []
    for shape in sizes:
        # construct input without any non-zero elements
        zeros = torch.zeros(shape, dtype=dtype, device=device, requires_grad=requires_grad)
        inputs.append(zeros)

        # construct input with mixed zero and non-zero elements
        mixed = make_arg(shape).requires_grad_(False)
        mask_t = make_tensor(shape, dtype=torch.bool, device=device, requires_grad=False)
        mixed[mask_t] = 0
        inputs.append(mixed)

    nonzero_sizes = [0, 1, XS, S, M]

    for input_t, nonzero_size in product(inputs, nonzero_sizes):
        yield SampleInput(input_t.clone().requires_grad_(requires_grad),
                          kwargs=dict(size=nonzero_size))

