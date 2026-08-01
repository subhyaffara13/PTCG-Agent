
def error_inputs_lstsq(op_info, device, **kwargs):
    zero_d = torch.randn((), device=device)
    yield ErrorInput(
        SampleInput(zero_d, args=(zero_d,)),
        error_type=RuntimeError,
        error_regex="at least 2 dimensions",
    )

