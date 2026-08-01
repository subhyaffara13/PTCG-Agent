
def error_inputs_adaptive_max_pool3d(opinfo, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32)

    # error inputs for incorrect input dimension
    yield ErrorInput(SampleInput(make_arg((2, 2, 2)), output_size=(2, 2, 2)),
                     error_type=ValueError, error_regex="Input dimension should be at least 4")

    # error inputs for empty output
    yield ErrorInput(SampleInput(make_arg((1, 2, 3, 4)), output_size=()),
                     error_regex="internal error")

    # error inputs for output_size lesser than 0
    yield ErrorInput(SampleInput(make_arg((1, 1, 1, 1, 1)), output_size=(-1, 0, 2)),
                     error_regex="Trying to create tensor with negative dimension")

