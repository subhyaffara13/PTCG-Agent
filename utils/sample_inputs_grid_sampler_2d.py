
def sample_inputs_grid_sampler_2d(op_info, device, dtype, requires_grad, **kwargs):
    # We get better tests if we change the range of the values to something like [-2,2]
    # because for grid (second tensor argument) the "useful" range is [-1,1] and this way
    # you get a better combination of out-of-range and in-range test cases
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad,
                           low=-2, high=2)

    batch_size = 2
    num_channels = 3
    modes = (0, 1, 2)
    align_cornerss = (False, True)
    padding_modes = (0, 1, 2)

    for mode, padding_mode, align_corners in itertools.product(modes, padding_modes, align_cornerss):
        yield SampleInput(
            _make_tensor((batch_size, num_channels, S, L)),
            _make_tensor((batch_size, M + 3, M, 2)),
            mode,
            padding_mode,
            align_corners,
        )

