
def error_inputs_gaussian_window(op_info, device, **kwargs):
    # Yield common error inputs
    yield from error_inputs_window(op_info, device, std=0.5, **kwargs)

    # Tests for negative standard deviations
    yield ErrorInput(
        SampleInput(3, std=-1, dtype=torch.float32, device=device, **kwargs),
        error_type=ValueError,
        error_regex="Standard deviation must be positive, got: -1 instead.",
    )

