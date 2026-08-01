
def bidirectional_mask_function(batch_idx: int, head_idx: int, q_idx: int, kv_idx: int) -> bool:
    """
    This creates a full bidirectional mask.

    NOTE: It is important to keep an index-based version for non-vmap expansion.
    """
    return q_idx >= 0

