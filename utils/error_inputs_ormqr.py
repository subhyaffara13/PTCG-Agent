
def error_inputs_ormqr(op_info, device, **kwargs):
    zero_d = torch.randn((), device=device)
    yield ErrorInput(SampleInput(zero_d, args=(zero_d, zero_d)), error_type=RuntimeError,
                     error_regex="input must have at least 2 dimensions")

    # https://github.com/pytorch/pytorch/issues/85218
    tensor_0 = torch.full((5, 0,), 1, device=device)
    tensor_1 = torch.full((5,), 1, device=device)
    tensor_2 = torch.full((5, 5,), 1, device=device)
    bool_3 = True
    bool_4 = True
    yield ErrorInput(SampleInput(tensor_0, args=(tensor_1, tensor_2, bool_3, bool_4)), error_type=RuntimeError,
                     error_regex=r"tau.shape\[-1\] must be equal to min\(other.shape\[-2\], input.shape\[-1\]\)")

