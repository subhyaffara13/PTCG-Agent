
def error_inputs_cat(op_info, device, **kwargs):

    make_arg = partial(make_tensor, device=device, dtype=torch.float32)

    # error inputs for more than one element of the written-to tensor refer to a single memory location
    yield ErrorInput(SampleInput([make_arg((S, S)), make_arg((S, S))],
                                 kwargs={'out': make_arg((1, S)).expand((2 * S, S))}),
                     error_regex='unsupported operation')

    # error inputs for empty tensors
    yield ErrorInput(SampleInput([], kwargs={'dim': 1}),
                     error_regex='non-empty list of Tensors', error_type=ValueError)

    # error inputs for different sizes
    yield ErrorInput(SampleInput([make_arg((S, S, L, L)), make_arg((S, 0, L - 1, L))], kwargs={'dim': 1}),
                     error_regex='Sizes of tensors must match except in dimension')
    yield ErrorInput(SampleInput([make_arg((S, 0, L - 1, L)), make_arg((S, S, L, L))], kwargs={'dim': 1}),
                     error_regex='Sizes of tensors must match except in dimension')

    # error inputs for different dimensions
    yield ErrorInput(SampleInput([make_arg((S - 1, 0)), make_arg((S, 0, L - 1, L))], kwargs={'dim': 1}),
                     error_regex='Tensors must have same number of dimensions')
    yield ErrorInput(SampleInput([make_arg((S, 0, L - 1, L)), make_arg((S - 1, 0))], kwargs={'dim': 1}),
                     error_regex='Tensors must have same number of dimensions')

    # error inputs for same memory locations
    x = torch.zeros((0), device=device)
    y = torch.randn((4, 6), device=device)

    err_msg = "the written-to tensor refer to a single memory location"

    yield ErrorInput(SampleInput((x, y), kwargs={'dim': 0, 'out': x}),
                     error_regex=err_msg)
    yield ErrorInput(SampleInput((x, y), kwargs={'dim': 0, 'out': y}),
                     error_regex=err_msg)

    z = torch.zeros((4, 6), device=device)
    yield ErrorInput(SampleInput((y, z), kwargs={'out': z[:2, :]}),
                     error_regex=err_msg)

    # error inputs for different devices
    if torch.device(device).type == 'cuda':
        x_cuda = make_tensor((3, 3), device=device, dtype=torch.float32)
        y_cpu = make_tensor((3, 3), device='cpu', dtype=torch.float32)
        yield ErrorInput(SampleInput((x_cuda, y_cpu)),
                         error_regex='Expected all tensors to be on the same device')

    # error inputs for different input sizes for more than 2 tensors
    yield ErrorInput(SampleInput([make_arg((L, 1)), make_arg((L, 1, 1)), make_arg((L, 1, 1))]),
                     error_regex='Tensors must have same number of dimensions')

    yield ErrorInput(SampleInput([make_arg((S, 1, M)), make_arg((S, 1, 1)), make_arg((S, M, 1))],
                                 kwargs={'dim': 1}),
                     error_regex='Sizes of tensors must match')

    # error inputs for None input
    yield ErrorInput(SampleInput((make_arg((S, 1, 1)), None)), error_type=TypeError,
                     error_regex='got None')

    # error inputs for zero-dimensional tensors
    yield ErrorInput(SampleInput([make_arg(()), make_arg(())]),
                     error_regex='zero-dimensional.*cannot be concatenated')

    # error inputs for different dtype of out tensors
    d = make_tensor((2, 3), device=device, dtype=torch.double if not device.startswith("mps") else torch.float16)
    x = make_tensor((2, 3), device=device, dtype=torch.float32)
    yield ErrorInput(SampleInput(x, kwargs={'out': d}), error_type=TypeError,
                     error_regex='invalid combination of arguments')

