
def error_inputs_max_pool1d(op_info, device, **kwargs):
    # Toggle requires_grad because `max_pool1d` has different path
    # based on whether `requires_grad` is set or not.
    for requires_grad in (True, False):
        make_arg = partial(make_tensor, device=device, dtype=torch.float, requires_grad=requires_grad)
        # error inputs when pad is negative
        x = make_arg((0, 1, 49))
        yield ErrorInput(SampleInput(x, kwargs={'kernel_size': 2, 'stride': 50, 'padding': -1, 'return_indices': True}),
                         error_regex='pad must be non-negative')

        # error inputs when pad > kernel_size / 2
        yield ErrorInput(SampleInput(x, kwargs={'kernel_size': 2, 'stride': 50, 'padding': 4, 'return_indices': True}),
                         error_regex='pad should be at most half of effective kernel size')

        # error inputs when pad > ((kernel_size - 1) * dilation + 1) / 2, when dilation is not default
        yield ErrorInput(SampleInput(x,
                         kwargs={'kernel_size': 3, 'dilation': 2, 'stride': 1, 'padding': 3, 'return_indices': True}),
                         error_regex='pad should be at most half of effective kernel size')

        # error inputs for input tensor
        error_msg = r'Expected 2D or 3D \(batch mode\) tensor with optional 0 dim batch size for input'
        yield ErrorInput(SampleInput(make_arg((), requires_grad=requires_grad), kwargs={'kernel_size': 1}),
                         error_regex=error_msg)

        # error inputs for empty input
        yield ErrorInput(SampleInput(torch.tensor([], device=device, requires_grad=requires_grad),
                                     kwargs={'kernel_size': 1}),
                         error_regex=error_msg)

        # error: unbatched input with 0 sized non-batch dims.
        yield ErrorInput(SampleInput(make_arg((0, 10), requires_grad=requires_grad),
                                     kwargs={'kernel_size': 1}),
                         error_regex=error_msg)

        # error: batched input with 0 sized non-batch dims.
        yield ErrorInput(SampleInput(make_arg((1, 10, 0), requires_grad=requires_grad),
                                     kwargs={'kernel_size': 1}),
                         error_regex=error_msg)

        # error inputs for empty input with stride=0
        error_msg = 'stride must be greater than zero, but got 0'
        yield ErrorInput(SampleInput(make_arg((3, 3, 3)), kwargs={'kernel_size': 1, 'stride': 0}),
                         error_regex=error_msg)

        # error inputs for empty input with dilation=0
        error_msg = 'dilation must be greater than zero, but got 0'
        yield ErrorInput(SampleInput(make_arg((3, 3, 3)),
                                     kwargs={'kernel_size': 1, 'stride': 1, 'padding': 0, 'dilation': 0}),
                         error_regex=error_msg)

        # error inputs for invalid output size
        error_msg = 'Invalid computed output size: -2'
        yield ErrorInput(SampleInput(make_arg((2, 2, 2)),
                                     kwargs={'kernel_size': 5, 'stride': 1, 'padding': 0, 'dilation': 1}),
                         error_regex=error_msg)

        # error inputs when kernel_size=0
        error_msg = 'kernel_size must be greater than zero'
        yield ErrorInput(SampleInput(x, kwargs={'kernel_size': 0}),
                         error_regex=error_msg)

        # error inputs for strides > 0
        error_msg = 'stride must be greater than zero'
        yield ErrorInput(SampleInput(x, kwargs={'kernel_size': 2, 'stride': 0}),
                         error_regex=error_msg)

