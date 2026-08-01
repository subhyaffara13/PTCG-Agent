
def error_inputs_native_layer_norm(opinfo, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32, requires_grad=False)
    input_shape = (1, 2, 3)

    err_msg1 = "Expected normalized_shape to be at least 1-dimensional"
    s1 = SampleInput(
        make_arg(input_shape), args=((), None, None, 1e-5)
    )
    yield ErrorInput(s1, error_regex=err_msg1)

    normalized_shape = (1, 2, 3)
    weight = make_arg((1, 2))
    err_msg2 = "Expected weight to be of same shape as normalized_shape"
    s2 = SampleInput(
        make_arg(input_shape), args=(normalized_shape, weight, None, 1e-5)
    )
    yield ErrorInput(s2, error_regex=err_msg2)

    bias = make_arg((1, 2))
    err_msg3 = "Expected bias to be of same shape as normalized_shape"
    s3 = SampleInput(
        make_arg(input_shape), args=(normalized_shape, None, bias, 1e-5)
    )
    yield ErrorInput(s3, error_regex=err_msg3)

    err_msg4 = "Given normalized_shape="
    s4 = SampleInput(
        make_arg((2, 2, 3)), args=((2, 2), None, None, 1e-5)
    )
    yield ErrorInput(s4, error_regex=err_msg4)

