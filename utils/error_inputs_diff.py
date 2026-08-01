
def error_inputs_diff(op_info, device, **kwargs):
    t = torch.rand((1, 3), device=device)
    n = -1
    yield ErrorInput(SampleInput(t, args=(n, ), kwargs=kwargs),
                     error_type=RuntimeError,
                     error_regex=f'order must be non-negative but got {n}')

