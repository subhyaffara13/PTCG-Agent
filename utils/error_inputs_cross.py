
def error_inputs_cross(op_info, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32)

    sample = SampleInput(input=make_arg((S, 3)), args=(make_arg((S, 1)),))
    err = "inputs dimension -1 must have length 3"
    yield ErrorInput(sample, error_regex=err, error_type=RuntimeError)

    sample = SampleInput(input=make_arg((5, S, 3)), args=(make_arg((S, 3)),))
    err = "inputs must have the same number of dimensions"
    yield ErrorInput(sample, error_regex=err, error_type=RuntimeError)

    sample = SampleInput(input=make_arg((S, 2)), args=(make_arg((S, 2)),))
    err = "must have length 3"
    yield ErrorInput(sample, error_regex=err, error_type=RuntimeError)

    sample = SampleInput(
        input=make_arg((S, 2)), args=(make_arg((S, 2)),), kwargs=dict(dim=2)
    )
    err = "Dimension out of range"
    yield ErrorInput(sample, error_regex=err, error_type=IndexError)

