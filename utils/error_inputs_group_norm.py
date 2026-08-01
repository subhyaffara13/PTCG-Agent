
def error_inputs_group_norm(opinfo, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32, requires_grad=False)

    # check that input has minimum number of dimensions
    err_msg1 = "Expected at least 2 dimensions for input tensor but received"
    s1 = SampleInput(make_arg(1), args=(1,))
    yield ErrorInput(s1, error_regex=err_msg1)

    # check that the channels dimension is compatible with number of groups
    err_msg2 = "Expected number of channels in input to be divisible by num_groups, but got input of shape"
    s2 = SampleInput(make_arg((2, 7, 4)), args=(2,))
    yield ErrorInput(s2, error_regex=err_msg2)

