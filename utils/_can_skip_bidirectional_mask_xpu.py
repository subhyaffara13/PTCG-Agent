
def _can_skip_bidirectional_mask_xpu(
    padding_mask: torch.Tensor | None,
    kv_length: int,
    local_attention_size: int | None,
) -> bool:
    """
    XPU-specific logic for determining if we can skip bidirectional mask creation.

    For XPU devices, we have special handling:
    - Skip if no padding and no local attention constraint
    """

    if is_tracing(padding_mask):
        return False

    # Check local attention constraint (same as CUDA)
    if local_attention_size is not None and kv_length >= local_attention_size:
        return False

    if padding_mask is None:
        # Without padding mask, can always skip for full bidirectional attention
        return True

    # Skip only if no padding tokens present
    return padding_mask.all()

