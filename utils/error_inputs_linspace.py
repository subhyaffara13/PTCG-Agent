
def error_inputs_linspace(op, device, **kwargs):
    yield ErrorInput(SampleInput(0, args=(3, -1)), error_type=RuntimeError, error_regex='number of steps must be non-negative')
    yield ErrorInput(
        SampleInput(0, args=(3, 1.)),
        error_type=TypeError,
        error_regex="received an invalid combination of arguments - got \\(int, int, float",
    )
    yield ErrorInput(
        SampleInput(torch.tensor([1, 1], device=device), args=(torch.tensor([3, 3], device=device), 1)),
        error_type=RuntimeError,
        error_regex="only supports 0-dimensional start and end tensors"
    )

