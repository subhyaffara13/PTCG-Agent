
def sample_inputs_grid_sampler_3d(op_info, device, dtype, requires_grad, **kwargs):
    _make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad,
                          low=-1, high=1)
    # Test both out-of-range and in-range grid values
    _make_grid = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad,
                         low=-4, high=4)

    modes = (0,)
    padding_modes = (0, 1, 2)
    align_cornerss = (False, True)
    shape_pairs = [
        # [input_shape, grid_shape]
        [(1, 1, 2, 2, 2), (1, 1, 1, 1, 3)],
        [(2, 3, S, L, L), (2, M + 2, M + 1, M, 3)],
        [(L, L + 1, L + 2, L + 3, L + 4), (L, M + 2, M + 1, M, 3)],
        [(M, M + 1, M + 2, M + 3, M + 4), (M, L + 3, L + 2, L + 1, 3)],
        [(L, M + 1, M + 2, M + 3, M + 4), (L, L + 3, L + 2, L + 1, 3)],
    ]

    params_prod = itertools.product(modes, padding_modes, align_cornerss, shape_pairs)

    for mode, padding_mode, align_corners, (input_shape, grid_shape) in params_prod:
        yield SampleInput(
            _make_input(input_shape),
            _make_grid(grid_shape),
            mode,
            padding_mode,
            align_corners,
        )

