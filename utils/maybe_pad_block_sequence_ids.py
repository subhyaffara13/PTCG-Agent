
def maybe_pad_block_sequence_ids(
    block_sequence_ids: torch.Tensor, attention_mask: torch.Tensor | None, kv_length: int, kv_offset: int
) -> torch.Tensor:
    """
    Pads the `block_sequence_ids` in case the total length is less than `kv_length`.
    Usually that happens with `StaticCache` generation or generating without cache.
    Pads to the right with `-1`.
    """
    if (padding_length := kv_length + kv_offset - block_sequence_ids.shape[-1]) > 0:
        block_sequence_ids = F.pad(block_sequence_ids, pad=(0, padding_length), value=-1)
    return block_sequence_ids

