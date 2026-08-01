
def sample_inputs_cosine_similarity(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as input_shape, dict of dim and eps
    cases: tuple[tuple, dict] = (  # type: ignore[assignment]
        ((S, S), {'dim': 1}),
        ((S, 2), {'dim': -1}),
        ((S,), {'dim': 0, 'eps': 0.5}),
        ((), {'dim': 0}),
        ((S, S, M), {'dim': 2}),
        ((S, S), {})
    )

    for input_shape, kwargs in cases:
        yield SampleInput(make_arg(input_shape), args=(make_arg(input_shape),), kwargs=kwargs)
    # Test for Broadcasting
    yield SampleInput(make_arg((1, 2, 3)), args=(make_arg((2, 1, 3)),), kwargs={'dim': -1})
    yield SampleInput(make_arg((1, 2, 3)), args=(make_arg((2, 1, 3)),), kwargs={'dim': -2})
    yield SampleInput(make_arg((2, 3)), args=(make_arg((2, 1, 3)),), kwargs={'dim': -1})

