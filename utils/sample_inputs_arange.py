
def sample_inputs_arange(op, device, dtype, requires_grad, **kwargs):
    int_samples = (
        # positive direction
        (-1, 2, 2),
        # negative direction
        (2, -3, -1),
        # start == end
        (1, 1, 1),
        (1, 1, -1),
        # divides evenly
        (0, -8, -4),
        (1, 5, 2),
        # bool
        (False, True, True),
        # default step
        (0, 1, None),
        # default start
        (None, 3, None),
    )

    def to_float(start, end, step):
        start = start + 0.1 if start is not None else None
        end = end + 0.1
        step = float(step) if step is not None else None
        return start, end, step

    float_samples = (
        # includes endpoint
        (0., -8. - 1e-6, -4.),
        (1., 5. + 1e-6, 2.),
        (0., -8., -4.),
        (1., 5., 2.),
        *(to_float(start, end, step) for (start, end, step) in int_samples),
    )

    large_samples = (
        (0, 10000, None),
    )

    samples = int_samples + float_samples
    if dtype not in (torch.int8, torch.uint8):
        samples += large_samples

    for start, end, step in samples:
        if start is None:
            if step is not None:
                raise AssertionError("Expected step to be None when start is None")
            # Pass end as positional arg
            yield SampleInput(end, kwargs={"dtype": dtype, "device": device})
            # (Similar to) calling torch.arange(end=3)
            yield SampleInput(0, kwargs={"end": end, "dtype": dtype, "device": device})
        elif step is None:
            yield SampleInput(start, args=(end,), kwargs={"dtype": dtype, "device": device})
        else:
            yield SampleInput(start, args=(end, step), kwargs={"dtype": dtype, "device": device})

    yield SampleInput(2)
    yield SampleInput(1, args=(3, 1))

