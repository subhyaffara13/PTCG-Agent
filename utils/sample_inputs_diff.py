
def sample_inputs_diff(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    test_cases = (
        ((1,), 0, None, None),
        ((S,), 0, None, None),
        ((S, 1), 0, None, None),
        ((S, 1), 1, None, None),
        ((S, S), 0, None, None),
        ((S, S), 1, None, None),
        ((S, S), 0, (1, S), (2, S)),
        ((S, S), 0, None, (2, S)),
        ((XS, XS, XS), 1, None, None),
        ((XS, XS, XS), 2, None, None),
        ((XS, XS, XS), 1, (XS, 1, XS), (XS, 1, XS)),
        ((XS, XS, XS), 2, (XS, XS, 1), (XS, XS, 1)),
        ((XS, XS, XS), 2, (XS, XS, XS), (XS, XS, XS)),)

    for size, dim, size_prepend, size_append in test_cases:
        prepend_size = 0 if (size_prepend is None) else size_prepend[dim]
        append_size = 0 if (size_append is None) else size_append[dim]
        dim_size = size[dim] + prepend_size + append_size
        for n in range(dim_size):
            input_tensor = make_arg(size)
            prepend = make_arg(size_prepend) if size_prepend else None
            append = make_arg(size_append) if size_append else None
            yield SampleInput(input_tensor, n, dim, prepend, append)

    # add some samples with n > dim_size
    yield SampleInput(make_arg((XS, XS, XS)), S + 1, 1)
    yield SampleInput(make_arg((XS, XS, XS)), S * 3 + 2, 2, make_arg((XS, XS, XS)), make_arg((XS, XS, XS)))

