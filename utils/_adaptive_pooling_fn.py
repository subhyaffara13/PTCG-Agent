import itertools

def _adaptive_pooling_fn(
    start_index, end_index, kernel_maxes, in_sizes, out_sizes, pooling_fn
):
    h_in, w_in = in_sizes
    h_out, w_out = out_sizes

    (
        h_start_index_fn,
        h_end_index_fn,
        w_start_index_fn,
        w_end_index_fn,
    ) = compute_indices_adaptive_pooling(
        start_index, end_index, h_in, w_in, h_out, w_out
    )

    def fn(idx, loader):
        *prefix, bh, bw = idx

        h_start_index = h_start_index_fn(bh)
        h_end_index = h_end_index_fn(bh)

        w_start_index = w_start_index_fn(bw)
        w_end_index = w_end_index_fn(bw)

        result = None
        for ih, iw in itertools.product(range(kernel_maxes[0]), range(kernel_maxes[1])):
            val = loader(
                prefix,
                [ih, iw],
                [h_start_index, w_start_index],
                [h_end_index, w_end_index],
            )
            if result is None:
                result = val
            else:
                result = pooling_fn(val, result)
        return result

    return fn

