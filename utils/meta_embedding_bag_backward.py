
def meta_embedding_bag_backward(
    grad,
    indices,
    offsets,
    offset2bag,
    bag_size,
    maximum_indices,
    num_weights,
    scale_grad_by_freq,
    mode,
    sparse,
    per_sample_weights,
    padding_idx=-1,
):
    if sparse:
        return aten._embedding_bag_sparse_backward(
            grad,
            indices,
            offsets,
            offset2bag,
            bag_size,
            num_weights,
            scale_grad_by_freq,
            mode,
            per_sample_weights,
            padding_idx,
        )
    else:
        return meta_embedding_bag_dense_backward(
            grad,
            indices,
            offset2bag,
            bag_size,
            maximum_indices,
            num_weights,
            scale_grad_by_freq,
            mode,
            per_sample_weights,
            padding_idx,
        )

