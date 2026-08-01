
def _make_3block_relative_position_ids(block_len: int) -> torch.Tensor:
    """Makes 3-blocked relative position ids for local attention."""
    position_ids = torch.arange(3 * block_len, dtype=torch.int32)
    center_position_ids = position_ids[block_len:-block_len]
    # [block_len, 3 * block_len]
    relative_position_ids = position_ids.unsqueeze(0) - center_position_ids.unsqueeze(1)
    return relative_position_ids

