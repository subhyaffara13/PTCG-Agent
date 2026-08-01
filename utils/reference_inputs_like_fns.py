
def reference_inputs_like_fns(op, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_like_fns(op, device, dtype, requires_grad, **kwargs)

    # shape
    cases = (
        (), (0,), (1, 0), (1, 1, 4, 5), (5, 3, 0, 1), (1, 4, 3, 1, 1)
    )

    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    for shape in cases:
        yield SampleInput(make_arg(shape))
        yield SampleInput(make_arg(shape).transpose(0, -1))
        yield SampleInput(make_arg(shape, noncontiguous=True))
        yield SampleInput(make_arg(shape, noncontiguous=True).transpose(0, -1))

