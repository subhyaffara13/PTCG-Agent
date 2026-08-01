
def reference_inputs_gaussian_window(op_info, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_window(op_info, device, dtype, requires_grad, **kwargs)

    cases = (
        (8, {"std": 0.1}),
        (16, {"std": 1.2}),
        (32, {"std": 2.1}),
        (64, {"std": 3.9}),
        (128, {"std": 4.5}),
        (256, {"std": 10}),
    )

    for size, kw in cases:
        yield SampleInput(size, sym=False, **kw)
        yield SampleInput(size, sym=True, **kw)

