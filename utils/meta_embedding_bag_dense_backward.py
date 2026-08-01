
def meta_embedding_bag_dense_backward(
    grad,
    indices,
    offset2bag,
    bag_size,
    maximum_indices,
    num_weights,
    scale_grad_by_freq,
    mode,
    per_sample_weights,
    padding_idx=-1,
):
    torch._check(
        grad.dtype in [torch.float16, torch.bfloat16, torch.float32, torch.float64],
        lambda: f"Unsupported input type encountered: {grad.dtype}",
    )
    if mode == MODE_MAX:
        torch._check(maximum_indices is not None)
    index_grad_weight = grad.new_empty((num_weights, grad.size(1)))
    return index_grad_weight

