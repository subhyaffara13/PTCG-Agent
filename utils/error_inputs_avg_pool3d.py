
def error_inputs_avg_pool3d(op_info, device, **kwargs):
    # error inputs when pad is negative
    x = torch.rand([0, 1, 49, 50], dtype=torch.float32)
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': 2, 'stride': 50, 'padding': -1}),
                     error_regex='pad must be non-negative')
    # 3-dimensional kernel
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': (3, 2, 2), 'stride': 50, 'padding': -1}),
                     error_regex='pad must be non-negative')

    # error inputs when pad > kernel_size / 2
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': 2, 'stride': 50, 'padding': 4}),
                     error_regex='pad should be at most half of effective kernel size')
    # 3-dimensional kernel
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': (3, 2, 2), 'stride': 50, 'padding': 4}),
                     error_regex='pad should be at most half of effective kernel size')

    # error inputs for zero divisor
    x = torch.zeros(3, 3, 3, 3)
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': (2, 2, 2), 'divisor_override': 0}),
                     error_regex='divisor must be not zero')

    # error inputs for invalid input dimension
    x = torch.rand([0, 1, 49], dtype=torch.float32)
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': 2, 'stride': 50, 'padding': 0}),
                     error_regex='non-empty 4D or 5D')

