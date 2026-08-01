
def _sparse_coo_flatten_indices(indices: Tensor, shape: tuple):
    # Flatted N-D indices to 1-D indices
    flat_indices = indices.new_zeros(indices.size(1))
    for d, sz in enumerate(shape):
        flat_indices.mul_(sz)
        flat_indices.add_(indices[d])
    return flat_indices

