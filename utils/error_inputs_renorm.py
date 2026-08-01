
def error_inputs_renorm(op_info, device, **kwargs):
    zero_d = torch.randn((), device=device)
    yield ErrorInput(SampleInput(zero_d, args=(0.5, 0, 1.0)), error_type=RuntimeError,
                     error_regex="needs at least 2 dimensions, got 0 dimensions")

