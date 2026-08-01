
def error_inputs_diag(op_info, device, **kwargs):
    zero_d = torch.randn((), device=device)
    yield ErrorInput(SampleInput(zero_d, args=(0,)), error_type=RuntimeError,
                     error_regex="1D or 2D")
    zero_d = torch.randn(1, 1, 1, device=device)
    yield ErrorInput(SampleInput(zero_d, args=(0,)), error_type=RuntimeError,
                     error_regex="1D or 2D")

