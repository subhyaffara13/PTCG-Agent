
def error_inputs_cauchy(op, device, **kwargs):
    t = torch.zeros([10], device=device)
    invalid_scale = 0
    yield ErrorInput(
        SampleInput(t, args=(0, invalid_scale,)),
        error_type=RuntimeError,
        error_regex=fr"cauchy_ expects sigma > 0.0, but found sigma={invalid_scale}",
    )

