
def error_inputs_normal(op, device, **kwargs):
    t = torch.zeros([10], device=device)
    invalid_std = -1
    yield ErrorInput(
        SampleInput(t, args=(0, invalid_std)),
        error_type=RuntimeError,
        error_regex=fr"normal expects std >= 0.0, but found std {invalid_std}",
    )

