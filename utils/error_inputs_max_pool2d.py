
def error_inputs_max_pool2d(op_info, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float, requires_grad=False)
    # error inputs when pad is negative
    x = make_arg((0, 1, 49))
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': 2, 'stride': 50, 'padding': -1, 'return_indices': True}),
                     error_regex='pad must be non-negative')
    # 2-dimensional kernel
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': (3, 2), 'stride': 50, 'padding': -1, 'return_indices': True}),
                     error_regex='pad must be non-negative')

    # error inputs when pad > kernel_size / 2 (kernel_size : int)
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': 2, 'stride': 50, 'padding': 4, 'return_indices': True}),
                     error_regex='pad should be at most half of effective kernel size')

    # error inputs when pad > kernel_size / 2 (kernel_size : tuple)
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': (3, 2), 'stride': 50, 'padding': 4, 'return_indices': True}),
                     error_regex='pad should be at most half of effective kernel size')

    # error: unbatched input with 0 sized non-batch dims.
    err_msg = r'Expected 3D or 4D \(batch mode\) tensor with optional 0 dim batch size for input'
    yield ErrorInput(SampleInput(make_arg((1, 0, 10)),
                                 kwargs={'kernel_size': 1}),
                     error_regex=err_msg)

    # error: batched input with 0 sized non-batch dims.
    yield ErrorInput(SampleInput(make_arg((2, 1, 10, 0)),
                                 kwargs={'kernel_size': 1}),
                     error_regex=err_msg)

    # error: inputs when kernel size too large for input
    yield ErrorInput(SampleInput(make_arg((1, 1, 4)),
                                 kwargs={'kernel_size': 2}),
                     error_regex='Output size is too small')

