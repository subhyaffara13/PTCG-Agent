
def _embedding_dense_backward(
    grad_output: torch.Tensor,
    indices: torch.Tensor,
    num_weights: int,
    padding_idx: int,
    scale_grad_by_freq: bool,
) -> torch.Tensor:
    # TODO: check if XE4 still need this fallback
    # check torch.xpu.get_device_properties(grad_output.device).architecture
    if grad_output.is_xpu:
        return NotImplemented
    # We can write a util function to update decomp table if we have more ops to fallback.
    return decomp_embedding_dense_backward(
        grad_output, indices, num_weights, padding_idx, scale_grad_by_freq
    )

