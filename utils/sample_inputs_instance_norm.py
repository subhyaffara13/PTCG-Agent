
def sample_inputs_instance_norm(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_arg_without_requires_grad = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)

    # Ordered as: input shape, kwargs for momentum, eps
    cases: tuple[tuple[int, ...], dict] = (
        ((S, S, S), {'momentum': 0.5, 'eps': 0.6}),
        ((S, S, S), {'momentum': 0.5, 'eps': 0.6, 'use_input_stats': True}),
        ((3, 2, 4), {'momentum': -1.2}),
        ((3, 2, 4), {'momentum': 0.0}),
        ((3, 2, 3, 4), {'momentum': -1.0, 'eps': 0.5}),
        ((3, 2, 3, 4), {'momentum': -1.0, 'eps': 0.5}),
    )

    for input_shape, kwargs in cases:
        # args: running mean, running var, weight and bias should necessarily be of shape: (channels,)
        channels = input_shape[1]
        weight = make_arg(channels)
        bias = make_arg(channels)
        running_mean = make_arg_without_requires_grad(channels, low=0)
        running_var = make_arg_without_requires_grad(channels, low=0)
        new_kwargs = {
            'running_mean': running_mean,
            'running_var': running_var,
            'weight': weight,
            'bias': bias,
            **kwargs
        }

        yield SampleInput(
            make_arg(input_shape),
            args=(),
            kwargs=new_kwargs
        )

    # Checking for permutations of weights and biases as `None`
    # instance_norm assumes that if there's a bias, there's a weight
    weights = [channels, None]
    biases = [None, None]

    for weight_channels, bias_channels in zip(weights, biases, strict=True):
        running_mean = make_arg_without_requires_grad(channels, low=0)
        running_var = make_arg_without_requires_grad(channels, low=0)
        yield SampleInput(
            make_arg(input_shape),
            args=(),
            kwargs={
                'running_mean': running_mean,
                'running_var': running_var,
                'weight': make_arg(weight_channels) if weight_channels is not None else None,
                'bias': make_arg(bias_channels) if bias_channels is not None else None
            }
        )

    # Test case for no optional kwargs
    yield SampleInput(make_arg((1, 2, 3)), kwargs={})

