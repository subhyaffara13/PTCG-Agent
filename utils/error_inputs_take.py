
def error_inputs_take(op_info, device, **kwargs):
    x = torch.rand((1,), device=device).expand((3,))
    src = torch.rand((6,), device=device)
    ind = torch.tensor([2, 1, 0], device=device, dtype=torch.int64)

    yield ErrorInput(SampleInput(src, args=(ind,), kwargs=dict(out=x)),
                     error_type=RuntimeError,
                     error_regex='unsupported operation')

    yield ErrorInput(SampleInput(src, args=(ind,), kwargs=dict(out=src)),
                     error_type=RuntimeError,
                     error_regex='unsupported operation')

    yield ErrorInput(SampleInput(ind.clone(), args=(ind[1:],), kwargs=dict(out=ind[:-1])),
                     error_type=RuntimeError,
                     error_regex='unsupported operation')

