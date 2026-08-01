
def meta_embedding_bag_per_sample_weights_backward(
    grad,
    weight,
    indices,
    offsets,
    offset2bag,
    mode,
    padding_idx=-1,
):
    embedding_features = grad.size(1)
    torch._check(
        mode == MODE_SUM,
        lambda: "embedding_bag_backward: per_sample_weights only supported for mode='sum'",
    )
    torch._check(grad.dim() == 2)
    torch._check(indices.dim() == 1)
    num_samples = indices.size(0)
    torch._check(weight.dim() == 2)
    torch._check(weight.size(1) == embedding_features)
    output = grad.new_empty((num_samples,))
    return output

