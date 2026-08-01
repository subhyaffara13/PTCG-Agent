
def _make_side_relative_position_ids(attention_mask: torch.Tensor, global_block_size: int) -> torch.Tensor:
    """Create the relative position tensor for local -> global attention."""
    block_ids, global_segment_ids = _make_global_fixed_block_ids(attention_mask, global_block_size)
    global_seq_len = global_segment_ids.shape[-1]
    global_positions = torch.arange(global_seq_len, device=block_ids.device)
    side_relative_position = global_positions - block_ids[..., None]
    return side_relative_position.type(torch.int64)

