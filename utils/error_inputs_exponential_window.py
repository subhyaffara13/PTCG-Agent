
def error_inputs_exponential_window(op_info, device, **kwargs):
    # Yield common error inputs
    yield from error_inputs_window(op_info, device, **kwargs)

    # Tests for negative decay values.
    yield ErrorInput(
        SampleInput(3, tau=-1, dtype=torch.float32, device=device, **kwargs),
        error_type=ValueError,
        error_regex="Tau must be positive, got: -1 instead.",
    )

    # Tests for symmetric windows and a given center value.
    yield ErrorInput(
        SampleInput(3, center=1, sym=True, dtype=torch.float32, device=device),
        error_type=ValueError,
        error_regex="Center must be None for symmetric windows",
    )

