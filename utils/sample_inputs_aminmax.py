
def sample_inputs_aminmax(op_info, device, dtype, requires_grad, **kwargs):
    test_cases: tuple[tuple, dict] = (  # type: ignore[assignment]
        ((S, S, S), {}),
        ((S, S, S), {'dim': 1}),
        ((S, S, S), {'dim': 1, 'keepdim': True}),
        ((), {'dim': 0}),
        ((), {}),
        ((), {'dim': 0, 'keepdim': True}),
        ((S, 0, S), {'dim': 0}),
    )

    for shape, kwargs in test_cases:
        yield SampleInput(
            make_tensor(shape, dtype=dtype, device=device, requires_grad=requires_grad),
            **kwargs)

