
def meta_embedding_dense_backward(
    grad_output,
    indices,
    num_weights,
    padding_idx,
    scale_grad_by_freq,
):
    grad_weight = grad_output.new_empty((num_weights, grad_output.size(-1)))
    return grad_weight

