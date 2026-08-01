
def sample_inputs_layer_norm(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Ordered as input shape, normalized_shape and a kwarg dict for eps
    cases: tuple[tuple[int, ...], tuple[int, ...], dict] = (
        ((1, 2, 3), (1, 2, 3), {'eps': 0.5}),
        ((2, 2, 3), (2, 3), {'eps': -0.5}),
        ((1,), (1,), {}),
        ((1, 2), (2,), {}),
        ((0, 1), (1,), {}),
    )

    for input_shape, normalized_shape, kwargs in cases:
        # Shape of weight and bias should be the same as normalized_shape
        weight = make_arg(normalized_shape)
        bias = make_arg(normalized_shape)
        yield SampleInput(
            make_arg(input_shape),
            args=(normalized_shape, weight, bias),
            kwargs=kwargs
        )
    # Without any optional args
    yield SampleInput(make_arg((1, 2)), args=((2,),))

