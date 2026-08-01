
def _get_reduce_scatter_tensors(
    state: _FSDPState, unsharded_grad: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Returns the input and output tensors to reduce-scatter, respectively.
    """
    chunks = list(unsharded_grad.chunk(state.world_size))
    numel_to_pad = state.world_size * chunks[0].numel() - unsharded_grad.numel()
    padded_unsharded_grad = (
        F.pad(unsharded_grad, [0, numel_to_pad]) if numel_to_pad > 0 else unsharded_grad
    )
    new_sharded_grad = torch.empty_like(chunks[0])  # padded
    return padded_unsharded_grad, new_sharded_grad

