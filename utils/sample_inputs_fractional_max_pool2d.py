
def sample_inputs_fractional_max_pool2d(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Order: input_shape, kernel_size
    cases = (((1, 3, 9, 9), 3),
             ((1, 3, 9, 9), (4, 4)),
             ((1, 3, 9, 9), (6, 6)),
             ((2, 3, 9, 9), (3, 3)),
             ((1, 1, 4, 4), (2, 2)),
             ((1, 2, 6, 6), (4, 4)))

    for input_shape, kernel_size in cases:
        for return_indices in [False, True]:
            # test case passing a single output size
            yield SampleInput(
                make_arg(input_shape),
                kernel_size,
                output_size=2,
                return_indices=return_indices,
            )

            # test case passing a tuple output size
            yield SampleInput(
                make_arg(input_shape),
                kernel_size,
                output_size=(2, 3),
                return_indices=return_indices,
            )

            # test case passing an output ratio
            yield SampleInput(
                make_arg(input_shape),
                kernel_size,
                output_ratio=(0.5, 0.5),
                return_indices=return_indices,
            )

    yield SampleInput(
        make_arg((1, 1, 16, 16)),
        (1, 1),
        output_ratio=(0.5, 0.5),
        return_indices=True,
        _random_samples=make_tensor((1, 1, 2), device=device, dtype=dtype, requires_grad=False),
    )

