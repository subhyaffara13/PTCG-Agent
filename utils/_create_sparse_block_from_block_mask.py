
def _create_sparse_block_from_block_mask(
    block_mask: tuple[Tensor, Tensor | None],
    mask_mod: _mask_mod_signature | None,
    seq_lengths: tuple[int, int],
    Q_BLOCK_SIZE: int = _DEFAULT_SPARSE_BLOCK_SIZE,
    KV_BLOCK_SIZE: int = _DEFAULT_SPARSE_BLOCK_SIZE,
) -> BlockMask:
    partial_blocks, full_blocks = block_mask

    partial_bm = _dense_to_ordered(partial_blocks)
    if full_blocks is not None:
        full_bm: tuple[Tensor | None, Tensor | None] = _dense_to_ordered(full_blocks)
    else:
        full_bm = (None, None)

    return BlockMask.from_kv_blocks(
        partial_bm[0],
        partial_bm[1],
        full_bm[0],
        full_bm[1],
        BLOCK_SIZE=(Q_BLOCK_SIZE, KV_BLOCK_SIZE),
        mask_mod=mask_mod,
        seq_lengths=seq_lengths,
    )

