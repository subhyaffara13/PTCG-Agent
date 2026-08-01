
def reference_inputs_group_norm(op_info, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_group_norm(
        op_info, device, dtype, requires_grad, **kwargs)

    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as input shape, num groups, and kwargs for eps
    cases: tuple[tuple[int, ...], int, float] = (
        ((20, 6, 10, 10), 3, {'eps' : 1e-5}),
        # equivalent with InstanceNorm
        # GroupNorm(C, num_groups=C) == InstanceNorm(num_features=C)
        ((20, 6, 10, 10), 6, {'eps' : 1e-5}),
        # equivalent with LayerNorm
        # GroupNorm(C, num_groups=1, affine=False) == LayerNorm(normalized_shape=[C, H, W], elementwise_affine=False)
        ((20, 6, 10, 10), 1, {'eps' : 1e-5}),
    )

    # num_channels is inferred to be input.shape[1] dimension
    for input_shape, num_groups, kwargs in cases:
        # Shape of weight and bias should be the same as num_channels
        channels = input_shape[1] if len(input_shape) > 1 else 0
        input_tensor = make_arg(input_shape)
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
            yield SampleInput(input_tensor, num_groups, **kwargs)

