
def sample_inputs_fractional_max_pool3d(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Order: input_shape, kernel_size
    cases = (((2, 3, 5, 5, 5), (2, 2, 2)),
             ((1, 2, 6, 5, 4), 2),
             ((1, 2, 5, 6, 5), (2, 3, 2)),
             ((1, 2, 6, 6, 6), (2, 3, 2)),
             ((1, 1, 7, 6, 7), (2, 3, 4)),
             ((1, 1, 4, 5, 4), (2, 2, 1)),
             ((1, 1, 8, 7, 6), (4, 3, 2)),
             ((0, 1, 4, 5, 4), (2, 2, 1)))

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
                output_size=(2, 3, 2),
                return_indices=return_indices,
            )

            # test case passing an output ratio
            yield SampleInput(
                make_arg(input_shape),
                kernel_size,
                output_ratio=(0.5, 0.5, 0.5),
                return_indices=return_indices,
            )

