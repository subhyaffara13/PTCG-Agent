
def sample_inputs_native_layer_norm(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as input shape, normalized_shape, eps
    cases: tuple[tuple[int, ...], tuple[int, ...], float] = (
        ((1, 2, 3), (1, 2, 3), 0.5),
        ((2, 2, 3), (2, 3), -0.5),
        ((1,), (1,), 1e-5),
        ((1, 2), (2,), 1e-5),
        ((0, 1), (1,), 1e-5),
    )

    for input_shape, normalized_shape, eps in cases:
        # Shape of weight and bias should be the same as normalized_shape
        weight = make_arg(normalized_shape)
        bias = make_arg(normalized_shape)
        yield SampleInput(
            make_arg(input_shape),
            args=(normalized_shape, weight, bias, eps),
        )
        yield SampleInput(
            make_arg(input_shape),
            args=(normalized_shape, None, bias, eps),
        )
        yield SampleInput(
            make_arg(input_shape),
            args=(normalized_shape, weight, None, eps),
        )
        yield SampleInput(
            make_arg(input_shape),
            args=(normalized_shape, None, None, eps),
        )

