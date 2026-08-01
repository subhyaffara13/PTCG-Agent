
def error_inputs_masked_select(op_info, device, **kwargs):
    x = torch.rand((1,), device=device).expand((3,))
    y = torch.rand((6,), device=device)
    mask = torch.tensor([True, False, True, True, False, False], device=device)

    yield ErrorInput(SampleInput(y, args=(mask,), kwargs=dict(out=x)),
                     error_type=RuntimeError,
                     error_regex='unsupported operation')

    yield ErrorInput(SampleInput(y, args=(mask,), kwargs=dict(out=y)),
                     error_type=RuntimeError,
                     error_regex='unsupported operation')

    yield ErrorInput(SampleInput(mask.clone(), args=(mask,), kwargs=dict(out=mask)),
                     error_type=RuntimeError,
                     error_regex='unsupported operation')

