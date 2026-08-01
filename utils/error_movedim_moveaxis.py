
def error_movedim_moveaxis(op_info, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32)

    # source length < destination length
    yield ErrorInput(
        SampleInput(make_arg(2, 3, 4, 5, 6), args=((3, -3), (1, 0, -1))),
        error_regex=(r"movedim: Invalid source or destination dims: source "
                     r"\(\[3, -3\] dims\) should contain the same number of "
                     r"dims as destination \(\[1, 0, -1\] dims\)"),
    )

    # source length > destination length
    yield ErrorInput(
        SampleInput(make_arg(2, 3, 4, 5, 6), args=((3, -3, 4), (1, 0))),
        error_regex=(r"movedim: Invalid source or destination dims: source "
                     r"\(\[3, -3, 4\] dims\) should contain the same number of "
                     r"dims as destination \(\[1, 0\] dims\)"),
    )

    # repeated source dim, with negative indices
    yield ErrorInput(
        SampleInput(make_arg(2, 3, 4, 5, 6), args=((0, 4, -5), (1, 0, 2))),
        error_regex=r"movedim: repeated dim in `source` \(\[0, 4, -5\]\)",
    )

    # repeated destination dim, with negative indices
    yield ErrorInput(
        SampleInput(make_arg(2, 3, 4, 5, 6), args=((1, 0, 2), (0, 4, -5))),
        error_regex=r"movedim: repeated dim in `destination` \(\[0, 4, -5\]\)",
    )

    # repeated dim (both), with negative indices
    yield ErrorInput(
        SampleInput(make_arg(2, 3, 4, 5, 6), args=((1, 0, -4), (0, 4, -5))),
        error_regex=r"movedim: repeated dim in `source` \(\[1, 0, -4\]\)",
    )

    # out of bounds source inputs, with negative indices
    yield ErrorInput(
        SampleInput(make_arg(2, 3, 4, 5, 6), args=((0, 1, -6), (1, 4, 2))),
        error_regex=r"Dimension out of range \(expected to be in range of \[-5, 4\], but got -6\)",
        error_type=IndexError,
    )

    # out of bounds destination inputs, with negative indices
    yield ErrorInput(
        SampleInput(make_arg(2, 3, 4, 5, 6), args=((1, 4, 2), (0, 1, -6))),
        error_regex=r"Dimension out of range \(expected to be in range of \[-5, 4\], but got -6\)",
        error_type=IndexError,
    )

    # out of bounds source input, int
    yield ErrorInput(
        SampleInput(make_arg(2, 3, 4, 5, 6), args=(-6, 1)),
        error_regex=r"Dimension out of range \(expected to be in range of \[-5, 4\], but got -6\)",
        error_type=IndexError,
    )

    # out of bounds destination input, int
    yield ErrorInput(
        SampleInput(make_arg(2, 3, 4, 5, 6), args=(3, -6)),
        error_regex=r"Dimension out of range \(expected to be in range of \[-5, 4\], but got -6\)",
        error_type=IndexError,
    )

