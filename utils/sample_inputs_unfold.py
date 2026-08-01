
def sample_inputs_unfold(op_info, device, dtype, requires_grad, **kwargs):
    test_cases = (
        ((), (0, 1, 1)),
        ((S, S, S, S), (0, 3, 1)),
        ((S, S, S, S), (1, 3, 1)),
        ((S, S, S, S), (2, 3, 1)),
        ((S, S, S, S), (3, 3, 1)),
        ((S, S, S, S), (0, 3, 2)),
        ((S, S, S, S), (1, 3, 2)),
        ((S, S, S, S), (2, 3, 2)),
        ((S, S, S, S), (3, 3, 2)),
        ((S, S, S, S), (0, 4, 1)),
        ((S, S, S, S), (1, 4, 1)),
        ((S, S, S, S), (2, 4, 1)),
        ((S, S, S, S), (3, 4, 1)),
        ((M,), (0, 3, 1)),
        ((M,), (0, 3, 2)),
        ((M,), (0, 3, 3)),
        ((1000,), (0, 3, 11)),
        ((1000,), (0, 2, 27)),
        ((10, 10), (0, 1, 2)),
        ((10, 10), (1, 2, 3)),
        ((10, 10), (1, 2, 2)),
        ((S, S, S), (2, 3, 2)),
    )

    for shape, arguments in test_cases:
        yield SampleInput(make_tensor(shape, dtype=dtype, device=device,
                                      low=None, high=None,
                                      requires_grad=requires_grad),
                          *arguments)

