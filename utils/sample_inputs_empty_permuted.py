
def sample_inputs_empty_permuted(op, device, dtype, requires_grad, **kwargs):
    # shape
    cases = (
        (), (0,), (1,), (1, 3, 5), (5, 3, 1), (1, 0, 5, 1),
    )

    for case in cases:
        for layout in itertools.permutations(range(len(case))):
            yield SampleInput(case, layout, device=device, dtype=dtype, requires_grad=requires_grad)

