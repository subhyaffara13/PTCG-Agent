
def sample_inputs_grid_sample(op_info, device, dtype, requires_grad, **kwargs):
    # We get better tests if we change the range of the values to something like [-2,2]
    # because for grid (second tensor argument) the "useful" range is [-1,1] and this way
    # you get a better combination of out-of-range and in-range test cases
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad,
                           low=-2, high=2)

    batch_size = 2
    num_channels = 3
    modes = ("bilinear", "nearest")
    align_cornerss = (False, True)
    padding_modes = ("zeros", "border", "reflection")

    for dim in (2, 3):

        modes_ = (*modes, "bicubic") if dim == 2 else modes

        for mode, padding_mode, align_corners in itertools.product(modes_, padding_modes, align_cornerss):
            yield SampleInput(
                _make_tensor((batch_size, num_channels, *[S] * dim)),
                _make_tensor((batch_size, *[S] * dim, dim)),
                mode=mode,
                padding_mode=padding_mode,
                align_corners=align_corners,
            )

