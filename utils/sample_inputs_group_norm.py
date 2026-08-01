
def sample_inputs_group_norm(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as input shape, num groups, and kwargs for eps
    cases: tuple[tuple[int, ...], int, float] = (
        ((1, 6, 3), 2, {'eps' : 0.5}),
        ((2, 6, 3), 2, {'eps' : -0.5}),
        ((1, 3), 1, {'eps' : 1e-5}),
        ((0, 2), 1, {'eps' : 1e-5}),
        ((S, S, S), 1, {'eps' : 0.5}),
    )

    # num_channels is inferred to be input.shape[1] dimension
    for input_shape, num_groups, kwargs in cases:
        # Shape of weight and bias should be the same as num_channels
        channels = input_shape[1] if len(input_shape) > 1 else 0
        weight_tensor = make_arg(channels)
        bias_tensor = make_arg(channels)

        # Checking for permutations of weights and biases as `None`
        weights = [weight_tensor, None]
        biases = [bias_tensor, None]
        for weight, bias in itertools.product(weights, biases):
            kwargs = {
                'weight': weight,
                'bias': bias,
                **kwargs
            }
            yield SampleInput(make_arg(input_shape), num_groups, **kwargs)

    # Without any optional args
    yield SampleInput(make_arg((1, 2)), args=(1,))

