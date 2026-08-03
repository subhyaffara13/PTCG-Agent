import itertools

def reference_inputs_permute(op, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_permute(op, device, dtype, requires_grad, **kwargs)

    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    cases = (
        ((), ()),
        ((1,), (0,)),
        ((2, 2), (1, 0)),
        ((2, 2), (0, 1)),
        ((2, 0, 1), (0, 2, 1)),
        ((3, 4, 2), (2, 1, 0)),
        ((3, 4, 2), (1, 0, 2)),
        ((3, 4, 2), (0, 1, 2)),
    )

    # Adds tricky permutations and permutations with noncontiguity
    for shape, permutation in cases:
        for p in itertools.permutations(permutation):
            a = make_arg(shape).permute(p)
            yield SampleInput(a, args=(permutation,))

            a = make_arg(shape, noncontiguous=True).permute(p)
            yield SampleInput(a, args=(permutation,))

