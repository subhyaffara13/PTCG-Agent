
def error_inputs_adaptive_avg_pool1d(opinfo, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32)

    # error inputs for empty output
    yield ErrorInput(SampleInput(make_arg((1, 2, 3)), output_size=()),
                     error_regex="'output_size' should contain one int")

    # error inputs for output_size lesser than 0
    yield ErrorInput(SampleInput(make_arg((1, 1, 1)), output_size=(-1,)),
                     error_regex="elements of output_size must be greater than or equal to 0")

