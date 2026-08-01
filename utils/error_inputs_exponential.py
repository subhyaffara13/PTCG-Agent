
def error_inputs_exponential(op, device, **kwargs):
    t = torch.zeros([10], device=device)
    invalid_rate = 0
    yield ErrorInput(
        SampleInput(t, args=(invalid_rate,)),
        error_type=RuntimeError,
        error_regex=fr"exponential_ expects lambda > 0.0, but found lambda={invalid_rate}",
    )

