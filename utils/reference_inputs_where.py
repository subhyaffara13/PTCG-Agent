
def reference_inputs_where(op, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_where(op, device, dtype, requires_grad, **kwargs)

    make_cond = partial(make_tensor, dtype=torch.bool, device=device, requires_grad=requires_grad)
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    # noncontiguous
    c = make_cond((10, 3), noncontiguous=True)
    a = make_arg((10, 1), noncontiguous=True)
    b = make_arg((3, 10, 3)).transpose(0, -1)

    # NOTE that the OpInfo for where takes samples of the form a, cond, b
    yield SampleInput(a, args=(c, b))

    # MPS does not support float64, which causes issues in the following tests
    if torch.device(device).type == "mps":
        return

    # type promoting
    # FIXME(rec): shouldn't other_dtype be used two lines below?
    other_dtype = torch.double if dtype is not torch.double else torch.long  # noqa: F841
    c = make_cond((10, 3), noncontiguous=True)
    a = make_arg((10, 1), dtype=torch.long)
    b = make_arg((10, 1))

    yield SampleInput(a, args=(c, b))

    # two python scalars
    c = make_cond((10, 3), noncontiguous=True)
    a = make_arg((1,)).item()
    b = make_arg((1,)).item()

    yield SampleInput(a, args=(c, b))

    # NaN propagation
    if dtype.is_floating_point or dtype.is_complex:
        if dtype.is_floating_point:
            nan = float('nan')
        else:
            # dtype.is_complex
            nan = complex(float('nan'), float('nan'))
        c = make_cond((1, 10, 3))
        a = make_arg((10, 3), noncontiguous=True)
        a[2, 1] = nan
        b = make_arg((1, 3))
        b[0, 2] = nan

        yield SampleInput(a, args=(c, b))

    # Python scalars type promotion
    for scalar in (0, 0.0, 2j, False):
        yield SampleInput(scalar, args=(c, b))
        yield SampleInput(a, args=(c, scalar))

