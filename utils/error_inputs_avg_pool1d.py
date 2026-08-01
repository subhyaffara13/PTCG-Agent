
def error_inputs_avg_pool1d(op_info, device, **kwargs):
    # error inputs when pad is negative
    x = torch.rand([0, 1, 49], dtype=torch.float32)
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': 2, 'stride': 50, 'padding': -1}),
                     error_regex='pad must be non-negative')

    # error inputs when pad > kernel_size / 2
    yield ErrorInput(SampleInput(x, kwargs={'kernel_size': 2, 'stride': 50, 'padding': 4}),
                     error_regex='pad should be at most half of effective kernel size')

