
def sample_inputs_histogramdd(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    sizes = ((S, S), (S, S, S), (S, 1, S), (S, 0, S))
    bin_ct_patterns = ((1, 1, 1, 1, 1), (2, 3, 2, 3, 2), (3, 2, 3, 2, 3))

    for size, bin_ct_pattern, weighted, density in product(sizes, bin_ct_patterns, [False, True], [False, True]):
        input_tensor = make_arg(size)
        bin_ct = bin_ct_pattern[:size[-1]]
        weight_tensor = make_arg(size[:-1]) if weighted else None

        yield SampleInput(input_tensor, bin_ct,
                          weight=weight_tensor, density=density)

        bins_tensor = [make_arg(ct + 1) for ct in bin_ct]
        yield SampleInput(input_tensor, bins_tensor,
                          weight=weight_tensor, density=density)

