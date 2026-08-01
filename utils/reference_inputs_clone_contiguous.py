
def reference_inputs_clone_contiguous(op, device, dtype, requires_grad, **kwargs):
    # NOTE: the default memory format for clone is torch.preserve_format, for contiguous it's torch.contiguous_format
    # This exploits that default to test torch.preserve_format for clone, without causing an error when testing contiguous
    yield from sample_inputs_clone_contiguous(op, device, dtype, requires_grad, **kwargs)

    shapes = (
        (3, 5, 6),
        (1, 1, 3, 5, 6),
        (1, 1, 3, 5, 6, 1, 1),
        (1, 0, 3, 5, 0, 2),
        (1, 0, 3, 5, 0, 0, 1, 1, 2),
        (),
    )

    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    for shape in shapes:
        yield SampleInput(make_arg(shape))
        yield SampleInput(make_arg(shape).transpose(0, -1))
        yield SampleInput(make_arg(shape, noncontiguous=True))
        yield SampleInput(make_arg(shape, noncontiguous=True).transpose(0, -1))

        yield SampleInput(make_arg(shape), kwargs={'memory_format': torch.contiguous_format})
        yield SampleInput(make_arg(shape).transpose(0, -1), kwargs={'memory_format': torch.contiguous_format})
        yield SampleInput(make_arg(shape, noncontiguous=True), kwargs={'memory_format': torch.contiguous_format})
        yield SampleInput(make_arg(shape, noncontiguous=True).transpose(0, -1), kwargs={'memory_format': torch.contiguous_format})

    # shape, strides, offset
    strided_cases = (
        ((5, 6, 2), (1, 1, 7), 2),
        ((5, 5, 4), (1, 1, 7), 2),
        ((5, 5, 2), (4, 5, 7), 3),
        ((5, 5, 2), (5, 5, 7), 3),
        ((5, 5, 2), (5, 5, 5), 3),
        ((9, 5, 2), (0, 1, 7), 3),
    )

    for shape, strides, offset in strided_cases:
        yield SampleInput(make_arg(500,).as_strided(shape, strides, offset))
        yield SampleInput(make_arg(500,).as_strided(shape, strides, offset), kwargs={'memory_format': torch.contiguous_format})

    # channels last 2D
    yield SampleInput(make_arg((2, 2, 2, 2)), kwargs={'memory_format': torch.channels_last})
    a = make_arg((2, 2, 2, 2)).permute(0, 3, 1, 2)
    yield SampleInput(a, kwargs={'memory_format': torch.channels_last})

    # channels last 3D
    yield SampleInput(make_arg((2, 2, 2, 2, 2)), kwargs={'memory_format': torch.channels_last_3d})
    a = make_arg((2, 2, 2, 2, 2)).permute(0, 4, 1, 2, 3)
    yield SampleInput(a, kwargs={'memory_format': torch.channels_last_3d})

