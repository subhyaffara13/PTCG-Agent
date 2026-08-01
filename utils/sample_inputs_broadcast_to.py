
def sample_inputs_broadcast_to(op_info, device, dtype, requires_grad, **kwargs):
    test_cases = (
        ((S, 1, 1), (S, S, S)),
        ((S, 1, S), (S, S, S)),
        ((S, 1), (S, S, S)),
        ((1,), (S, S, S)),
        ((1, S), (1, 1, S)),
        ((), ()),
        ((), (1, 3, 2)),
    )

    return (
        SampleInput(
            make_tensor(size, dtype=dtype, device=device, low=None, high=None, requires_grad=requires_grad),
            shape,
        ) for size, shape in test_cases)

