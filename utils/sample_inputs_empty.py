
def sample_inputs_empty(op, device, dtype, requires_grad, **kwargs):
    # shape
    cases = (
        (), (0,), (1,), (1, 3, 5), (5, 3, 1), (1, 0, 5, 1),
    )

    for case in cases:
        yield SampleInput(case, device=device, dtype=dtype, requires_grad=requires_grad)

