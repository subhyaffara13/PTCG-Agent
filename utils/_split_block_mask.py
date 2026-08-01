
def _split_block_mask(
    block_mask: BlockMask,
    num_chunks: int,
) -> list[BlockMask]:
    """Given a block mask, split the block mask along the batch dimension (dim0).

    Args:
        block_mask: Block mask to split
        num_chunks: Number of chunks to split the block mask into

    Returns:
        chunk_block_masks: List of chunked block masks
    """

    # BlockMask will broadcast if B is 1.
    if block_mask.kv_num_blocks.size(0) == 1:
        return [block_mask] * num_chunks

    if not block_mask.kv_num_blocks.size(0) >= num_chunks:
        raise AssertionError(
            "Block mask has fewer batch size than the number of chunks. "
        )

    batch_dim = 0
    kv_num_blocks_chunks = torch.tensor_split(
        block_mask.kv_num_blocks, num_chunks, batch_dim
    )
    kv_indices_chunks = torch.tensor_split(block_mask.kv_indices, num_chunks, batch_dim)
    full_kv_num_blocks_chunks = (
        torch.tensor_split(block_mask.full_kv_num_blocks, num_chunks, batch_dim)
        if block_mask.full_kv_num_blocks is not None
        else [None] * num_chunks
    )
    full_kv_indices_chunks = (
        torch.tensor_split(block_mask.full_kv_indices, num_chunks, batch_dim)
        if block_mask.full_kv_indices is not None
        else [None] * num_chunks
    )

    chunk_block_masks = []
    batch_offset = 0
    for chunk_idx in range(num_chunks):

        def create_mask_mod(idx):
            def batch_offset_mask_mod(b, h, q_idx, kv_idx):
                b_offset = torch.full_like(b, idx)
                return block_mask.mask_mod(b + b_offset, h, q_idx, kv_idx)

            return batch_offset_mask_mod

        chunk_block_masks.append(
            BlockMask.from_kv_blocks(
                kv_num_blocks=kv_num_blocks_chunks[chunk_idx],
                kv_indices=kv_indices_chunks[chunk_idx],
                full_kv_num_blocks=full_kv_num_blocks_chunks[chunk_idx],
                full_kv_indices=full_kv_indices_chunks[chunk_idx],
                BLOCK_SIZE=block_mask.BLOCK_SIZE,
                mask_mod=create_mask_mod(batch_offset),
                seq_lengths=block_mask.seq_lengths,
            )
        )
        batch_offset += kv_num_blocks_chunks[chunk_idx].size(0)
    return chunk_block_masks

