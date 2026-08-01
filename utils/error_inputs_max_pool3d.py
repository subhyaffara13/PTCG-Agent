
def error_inputs_max_pool3d(op_info, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float, requires_grad=False)
    # error inputs when pad is negative
    x = make_arg((0, 1, 49, 50))
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': 2, 'stride': 50, 'padding': -1, 'return_indices': True}),
                     error_regex='pad must be non-negative')
    # 3-dimensional kernel
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': (3, 2, 2), 'stride': 50,
                                            'padding': -1, 'return_indices': True}),
                     error_regex='pad must be non-negative')

    # error inputs when pad > kernel_size / 2 (kernel_size: int)
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': 2, 'stride': 50, 'padding': 4, 'return_indices': True}),
                     error_regex='pad should be at most half of effective kernel size')

    # error inputs when pad > kernel_size / 2 (kernel_size: tuple)
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': (3, 2, 2), 'stride': 50,
                                            'padding': 4, 'return_indices': True}),
                     error_regex='pad should be at most half of effective kernel size')

    # error: unbatched input with 0 sized non-batch dims.
    err_msg = r'Expected input\'s non-batch dimensions to have positive length'
    yield ErrorInput(SampleInput(make_arg((0, 1, 2, 10)),
                                 kwargs={'kernel_size': 1}),
                     error_regex=err_msg)

    # error: batched inputs with 0 sized non-batch dims.
    yield ErrorInput(SampleInput(make_arg((2, 1, 0, 1, 2)),
                                 kwargs={'kernel_size': 1}),
                     error_regex=err_msg)

    # error: inputs when kernel size too large for input
    yield ErrorInput(SampleInput(make_arg((1, 1, 1, 4, 4)),
                                 kwargs={'kernel_size': 2}),
                     error_regex='Output size is too small')

