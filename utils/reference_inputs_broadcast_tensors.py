
def reference_inputs_broadcast_tensors(op, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_broadcast_tensors(op, device, dtype, requires_grad, **kwargs)

    m = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    n = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad, noncontiguous=True)

    cases = (
        ((), (1, 1), (1, 1, 7, 1), (3, 1, 1)),
        ((3, 5, 6), (1, 3, 5, 6), (1, 1, 1, 1, 6), (8, 3, 5, 6))
    )

    for a, b, c, d in cases:
        yield SampleInput(m(a), args=(m(b), m(c), m(d)))
        yield SampleInput(n(a), args=(n(b), n(c), n(d)))

