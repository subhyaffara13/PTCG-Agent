
def sample_inputs_avgpool1d(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Order: input_shape, kernel_size, kwargs
    cases: list[tuple[tuple[int, ...], int | tuple[int, ...], dict]] = [
        ((2, 3, 9), (3,), {}),
        ((1, 3, 9), 3, dict(stride=1, padding=1, ceil_mode=True, count_include_pad=False)),
        ((1, 3, 9), (6,), dict(stride=(3,), padding=(2,), ceil_mode=True, count_include_pad=True)),
        ((2, 3, 9), (3,), dict(stride=(1,), padding=(1,), ceil_mode=False, count_include_pad=True)),
        ((0, 3, 9), (6,), dict(stride=(3,), padding=(2,), ceil_mode=False, count_include_pad=True)),
        ((1, 2, 9), (7,), dict(stride=(3,), padding=(2,), ceil_mode=False)),
        ((1, 2, 9), (7,), dict(stride=(3,), padding=(3,), ceil_mode=True)),
        ((1, 2, 9), (7,), dict(stride=(3,), ceil_mode=False)),
        ((1, 2, 9), (7,), dict(stride=(3,), ceil_mode=True)),
    ]

    for input_shape, kernel_size, kwargs in cases:
        yield SampleInput(make_arg(input_shape), args=(kernel_size,), kwargs=kwargs)

