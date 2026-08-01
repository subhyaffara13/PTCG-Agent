
def error_inputs_kaiser_window(op_info, device, **kwargs):
    # Yield common error inputs
    yield from error_inputs_window(op_info, device, beta=12, **kwargs)

    # Tests for negative beta
    yield ErrorInput(
        SampleInput(3, beta=-1, dtype=torch.float32, device=device, **kwargs),
        error_type=ValueError,
        error_regex="beta must be non-negative, got: -1 instead.",
    )

