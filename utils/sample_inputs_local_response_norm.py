
def sample_inputs_local_response_norm(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as input shape, size and a kwarg dict for alpha, beta, and k
    cases: tuple[tuple[int, ...], tuple[int, ...], dict] = (
        ((1, 6, 3), 2, {'alpha': 3e-05, 'beta': 0.5, 'k': 1.25}),
        ((1, 6, 3), 2, {'beta': 0.5, 'k': 1.25}),
        ((1, 6, 3), 2, {'alpha': 3e-05, 'k': 1.25}),
        ((1, 6, 3), 2, {'alpha': 3e-05, 'beta': 0.5}),
        ((1, 6, 3), 2, {'alpha': 3e-05}),
        ((1, 6, 3), 2, {'beta': 0.5}),
        ((1, 6, 3), 2, {'k': 1.25}),
        ((1, 6, 3), 2, {}),
        ((2, 6, 3), 2, {'alpha': 3e-05, 'beta': 0.5, 'k': 1.25}),
        ((1, 1, 2), 1, {'alpha': 3e-05, 'beta': 0.5, 'k': 1.25}),
        ((0, 1, 2), 1, {'alpha': 3e-05, 'beta': 0.5, 'k': 1.25}),
    )

    for input_shape, size, kwargs in cases:
        yield SampleInput(make_arg(input_shape), args=(size,), kwargs=kwargs)

