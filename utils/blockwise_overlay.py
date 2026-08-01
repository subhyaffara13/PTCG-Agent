
def blockwise_overlay(block_sequence_ids: torch.Tensor) -> Callable:
    """
    This is an overlay depicting a blockwise masking pattern. Instead of a single
    token, each block consists of arbitrary length tokens. In causal setup, each block
    can attend to prev block causally and can't attend to future blocks. Within one block
    the attention is always bidirectional.
    Mostly used in MLLMs when non-text data attends bidirectionally to itself.
    """

    def inner_mask(batch_idx: int, head_idx: int, q_idx: int, kv_idx: int) -> bool:
        # Unmask if the q and kv come from same group which is not -1 (i.e. non-text)
        q_group = block_sequence_ids[batch_idx, q_idx]
        kv_group = block_sequence_ids[batch_idx, kv_idx]
        return (q_group == kv_group) & (q_group >= 0)

    return inner_mask

