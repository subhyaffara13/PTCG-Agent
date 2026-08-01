
def error_inputs_conv2d(opinfo, device, **kwargs):
    dtype = highest_precision_float(device)
    cdtype = highest_precision_complex(device)
    make_arg = partial(make_tensor, device=device, dtype=dtype)
    make_int_arg = partial(make_tensor, device=device, dtype=torch.int64)
    make_complex_arg = partial(make_tensor, device=device, dtype=cdtype)

    # error inputs for different dtypes of input tensor and bias
    yield ErrorInput(
        SampleInput(make_int_arg((2, 4, 4)), args=(make_int_arg((3, 2, 3, 3)), make_arg((3,)))),
        error_regex="should be the same")

    # error inputs for different dtypes of input tensor and bias
    yield ErrorInput(
        SampleInput(make_arg((2, 4, 4)), args=(make_arg((3, 2, 3, 3)), make_complex_arg((3,)))),
        error_regex="should be the same")

    # error inputs for negative strides
    yield ErrorInput(
        SampleInput(make_arg((1, 1, 4, 4)), args=(make_arg((1, 2, 2, 3)), make_arg((1,))),
                    kwargs={'stride': (-1,)}), error_regex="non-positive stride is not supported")

    # error inputs for negative padding
    yield ErrorInput(
        SampleInput(make_arg((1, 1, 4, 3)), args=(make_arg((1, 2, 2, 4)), make_arg((1,))),
                    kwargs={'padding': (-1,)}), error_regex="negative padding is not supported")

    # error inputs for negative dilation
    yield ErrorInput(
        SampleInput(make_arg((1, 1, 4, 2)), args=(make_arg((1, 1, 2, 5)), make_arg((1,))),
                    kwargs={'dilation': (-1,)}), error_regex="dilation should be greater than zero")

    # FIXME: https://github.com/pytorch/pytorch/issues/85656
    # error inputs for bias shape not equal to the output channels
    # yield ErrorInput(SampleInput(make_arg((1, 1, 4, 4)), args=(make_arg((1, 1, 3, 2)), make_arg((2,)))),
    #                  error_regex="expected bias to be 1-dimensional with 1 elements")

    # error inputs for input.ndim != weight.ndim
    yield ErrorInput(
        SampleInput(make_arg((1, 1, 4, 3)), args=(make_arg((1, 2, 2)), make_arg((1,))),
                    kwargs={'padding': 'same'}), error_regex="Expected 3-dimensional input for 3-dimensional weight")

    # error inputs for the weight[0] are less than the number of groups
    yield ErrorInput(
        SampleInput(make_arg((2, 2, 4, 3)), args=(make_arg((2, 2, 1, 3)), make_arg((2,))),
                    kwargs={'groups': 3}), error_regex="expected weight to be at least 3 at dimension 0")

    # error inputs for groups the weight[0] are less than the number of groups
    yield ErrorInput(
        SampleInput(make_arg((2, 2, 4, 3)), args=(make_arg((2, 2, 1, 3)), make_arg((2,))),
                    kwargs={'padding': 'same', 'groups': 3}), error_regex="expected weight to be at least 3 at dimension 0")

    # error inputs for invalid groups
    yield ErrorInput(
        SampleInput(make_arg((2, 2, 4, 5)), args=(make_arg((2, 2, 1, 4)), make_arg((2,))),
                    kwargs={'padding': 'same', 'groups': -1}), error_regex="non-positive groups is not supported")

    # error inputs for invalid groups
    yield ErrorInput(
        SampleInput(make_arg((2, 2, 4, 3)), args=(make_arg((2, 2, 4, 3)), make_arg((2,))),
                    kwargs={'padding': 'same', 'groups': 0}), error_regex="non-positive groups is not supported")

