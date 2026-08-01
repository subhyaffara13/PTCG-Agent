
def sample_trapezoid(op_info, device, dtype, requires_grad, **kwargs):
    y_shape_x_shape_and_kwargs = [
        ((2, 3), (2, 3), {}),
        ((2, 3), (2, 3), {'dim': 1}),
        ((6,), (6,), {}),
        ((6,), None, {}),
        # When 'trapezoid' is called with an empty input, it does not produce an output with requires_grad
        # See Issue #{61619}
        # ((6,0), (6,0), {}),
        ((2, 3), (1, 3), {}),
        ((3, 3), (3, 3), {}),
        ((3, 3), (3, 3), {'dim': -2}),
        ((5,), None, {'dx': 2.0}),
        ((2, 2), None, {'dx': 3.0})
    ]
    make_arg = partial(make_tensor, dtype=dtype, device=device, low=None, high=None,
                       requires_grad=requires_grad)
    for y_shape, x_shape, kwarg in y_shape_x_shape_and_kwargs:
        y_tensor = make_arg(y_shape)
        if x_shape is not None:
            x_tensor = make_arg(x_shape)
            yield SampleInput(y_tensor, x_tensor, **kwarg)
        else:
            yield SampleInput(y_tensor, **kwarg)

