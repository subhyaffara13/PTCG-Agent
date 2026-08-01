
def error_inputs_geometric(op, device, **kwargs):
    t = torch.zeros([10], device=device)
    neg_prob = -1
    yield ErrorInput(
        SampleInput(t, args=(neg_prob,)),
        error_type=RuntimeError,
        error_regex=fr"geometric_ expects p to be in \(0, 1\), but got p={neg_prob}",
    )

