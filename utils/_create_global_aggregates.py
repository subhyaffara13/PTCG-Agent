
def _create_global_aggregates(
    hidden_states: torch.Tensor, block_ids: torch.Tensor, global_seq_len: int
) -> torch.Tensor:
    """Compute individual block aggregates by summing over individual blocks."""
    # (batch..., seq_len, global_seq_len))
    block_ids = block_ids.where(
        block_ids >= 0, torch.tensor(global_seq_len, dtype=block_ids.dtype, device=block_ids.device)
    )
    one_hot_block_ids = nn.functional.one_hot(block_ids.type(torch.int64), global_seq_len + 1)[:, :, :-1]
    return torch.einsum("...nd,...ng->...gd", hidden_states, one_hot_block_ids.type(hidden_states.dtype))

