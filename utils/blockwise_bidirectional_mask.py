
def blockwise_bidirectional_mask(block_boundaries: torch.Tensor) -> Callable:
    def inner_mask(batch_idx: int, head_idx: int, q_idx: int, kv_idx: int) -> bool:
        q_block = torch.bucketize(q_idx, block_boundaries)
        kv_block = torch.bucketize(kv_idx, block_boundaries)
        return kv_block <= q_block

    return inner_mask

