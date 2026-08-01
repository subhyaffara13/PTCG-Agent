
def error_inputs_uniform(op, device, **kwargs):
    t = torch.zeros([10], device=device)
    yield ErrorInput(
        SampleInput(t, args=(3, -1)),
        error_type=RuntimeError,
        error_regex=r"uniform_ expects to return a \[from, to\) range, but found from=3 > to=-1",
    )

