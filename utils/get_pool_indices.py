
def get_pool_indices(feature_lens: torch.Tensor, kwargs: dict | None = None) -> torch.Tensor:
    """Compute indices for post-encoder stride-2 average pooling, or pop `"pool_indices"` from `kwargs` if precomputed.

    Args:
        feature_lens: `(batch_size,)` mel spectrogram lengths.
        kwargs: optional caller kwargs — if it contains `"pool_indices"` it is popped and returned.

    Returns:
        `(total_pooled,)` flat index of first element of each stride-2 pair.
    """
    if kwargs is not None and (pool_indices := kwargs.pop("pool_indices", None)) is not None:
        return pool_indices
    after_conv1 = (feature_lens - 1) // 2 + 1
    num_pooled = (after_conv1 - 2) // 2 + 1
    offsets = F.pad(after_conv1[:-1].cumsum(0), (1, 0), value=0)
    pair_offsets = torch.repeat_interleave(offsets, num_pooled)
    local_indices = torch.arange(num_pooled.sum(), device=feature_lens.device)
    local_indices -= torch.repeat_interleave(F.pad(num_pooled[:-1].cumsum(0), (1, 0), value=0), num_pooled)
    return pair_offsets + local_indices * 2


def get_pool_indices(feature_lens: torch.Tensor, kwargs: dict | None = None) -> torch.Tensor:
    """Compute indices for post-encoder stride-2 average pooling, or pop `"pool_indices"` from `kwargs` if precomputed.

    Args:
        feature_lens: `(batch_size,)` mel spectrogram lengths.
        kwargs: optional caller kwargs — if it contains `"pool_indices"` it is popped and returned.

    Returns:
        `(total_pooled,)` flat index of first element of each stride-2 pair.
    """
    if kwargs is not None and (pool_indices := kwargs.pop("pool_indices", None)) is not None:
        return pool_indices
    after_conv1 = (feature_lens - 1) // 2 + 1
    num_pooled = (after_conv1 - 2) // 2 + 1
    offsets = F.pad(after_conv1[:-1].cumsum(0), (1, 0), value=0)
    pair_offsets = torch.repeat_interleave(offsets, num_pooled)
    local_indices = torch.arange(num_pooled.sum(), device=feature_lens.device)
    local_indices -= torch.repeat_interleave(F.pad(num_pooled[:-1].cumsum(0), (1, 0), value=0), num_pooled)
    return pair_offsets + local_indices * 2

