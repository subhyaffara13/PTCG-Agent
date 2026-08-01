
def error_inputs_index_select(op_info, device, **kwargs):
    x = torch.rand((1, 6), device=device).expand((2, 6))
    y = torch.rand((3, 6), device=device)
    ind = torch.tensor([0, 1], dtype=torch.int64, device=device)

    yield ErrorInput(SampleInput(y, args=(1, ind,), kwargs=dict(out=x)),
                     error_type=RuntimeError,
                     error_regex='unsupported operation')

