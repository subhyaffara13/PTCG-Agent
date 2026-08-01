
def sample_inputs_cat_concat(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    cases: tuple[tuple, tuple, dict] = (  # type: ignore[assignment]
        ((S, S), (S, S), {'dim': -1}),
        ((S, S), (S, S), {'dim': 1}),
        ((M, S), (S, S), {'dim': 0}),  # different shapes
        ((1, 2, 3), (1, 2, 3), {'dim': -2}),
        ((0,), (0,), {'dim': 0}),  # empty tensor
        ((0,), (S, S), {'dim': 1}),  # empty tensor with unempty and dim=1 (special case for legacy_cat_wrap_dim)
        ((0, S), (S, S), {'dim': 0}),
        ((1,), (1,), {})  # dim not passed, fallback to default
    )

    for input_shape1, input_shape2, kwargs in cases:
        yield SampleInput([make_arg(input_shape1), make_arg(input_shape2)], kwargs=kwargs)

    # from coat_lite_mini
    yield SampleInput([make_arg((2, 2, 2, 2), memory_format=torch.channels_last)], args=(1,),)

