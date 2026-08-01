
def sample_inputs_avgpool3d(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Order: input_shape, kernel_size, stride, padding, ceil_mode, count_include_pad, divisor_override
    cases: list[tuple[tuple[int, ...], int | tuple[int, ...], dict]] = [
        ((2, 3, 3, 4, 4), (2, 2, 2), {}),
        ((1, 2, 4, 4, 4), 2, dict(stride=1, padding=1, ceil_mode=True,
                                  count_include_pad=False, divisor_override=2)),
        ((1, 2, 5, 5, 5), (2, 3, 4), dict(stride=(1, 2, 2), padding=(0, 1, 2), ceil_mode=True,
                                          count_include_pad=True, divisor_override=2)),
        ((1, 2, 5, 5, 5), (2, 3, 4), dict(stride=(1, 2, 2), padding=(0, 1, 2), ceil_mode=False)),
        ((1, 1, 7, 5, 7), (6, 3, 4), dict(stride=(2, 3, 2), padding=(3, 1, 0), ceil_mode=False,
                                          count_include_pad=False, divisor_override=2)),
        ((1, 1, 4, 5, 4), (2, 2, 3), dict(stride=(2, 2, 1), padding=0, ceil_mode=False,
                                          count_include_pad=True, divisor_override=-2)),
        ((1, 1, 6, 5, 6), (4, 5, 6), dict(stride=(2, 3, 2), padding=2, ceil_mode=True,
                                          count_include_pad=True, divisor_override=None)),
        ((0, 1, 4, 5, 4), (2, 3, 1), dict(stride=(2, 1, 2), padding=0, ceil_mode=False,
                                          count_include_pad=True, divisor_override=None)),
    ]

    for input_shape, kernel_size, kwargs in cases:
        yield SampleInput(make_arg(input_shape), args=(kernel_size,), kwargs=kwargs)

