
def noop_mask(
    batch: Tensor,
    head: Tensor,
    token_q: Tensor,
    token_kv: Tensor,
) -> Tensor:
    """Returns a noop mask_mod"""
    return batch.new_ones(size=(), dtype=torch.bool, device=batch.device)

