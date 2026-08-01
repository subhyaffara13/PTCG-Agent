
def _low_memory_max_pool_offsets_to_indices(
    offsets, kernel_size, input_size, stride, padding, dilation
):
    # TODO: Generalize to other max pooling flavors
    n_dim = len(kernel_size)

    def increments_to_index(idx, reduction_idx):
        bh = idx[-n_dim:]
        return [
            (bh[i] * stride[i]) + (reduction_idx[i] * dilation[i]) - padding[i]
            for i in range(n_dim)
        ]

    return _pool_offsets_to_indices(
        offsets, kernel_size, input_size, increments_to_index
    )

