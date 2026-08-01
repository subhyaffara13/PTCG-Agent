
def sample_inputs_histogram(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    sizes = ((), (S,), (S, S), (S, S, S), (S, 1, S), (S, 0, S))

    for size, bin_ct, weighted, density in product(sizes, range(1, 5), [False, True], [False, True]):
        input_tensor = make_arg(size)
        weight_tensor = make_arg(size) if weighted else None

        yield SampleInput(input_tensor, bin_ct,
                          weight=weight_tensor, density=density)

        bins_tensor = make_arg((bin_ct + 1,))
        sorted_bins, _bins_indices = torch.sort(bins_tensor)
        yield SampleInput(input_tensor, sorted_bins,
                          weight=weight_tensor, density=density)

