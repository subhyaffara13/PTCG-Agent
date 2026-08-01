
def _create_empty_block_mask(query: Tensor, key: Tensor) -> BlockMask:
    r"""Default block mask for flex attention.
    If users don't specify any block sparse mask info, we create this
    empty block sparse mask. Which creates a BlockMask with 1 block that is the full length
    of the query and key tensors.
    """
    device = query.device
    return BlockMask.from_kv_blocks(
        kv_num_blocks=torch.ones([1, 1, 1], dtype=torch.int32, device=device),
        kv_indices=torch.zeros([1, 1, 1, 1], dtype=torch.int32, device=device),
        BLOCK_SIZE=_LARGE_SPARSE_BLOCK_SIZE,
        seq_lengths=(1, 1),
    )

