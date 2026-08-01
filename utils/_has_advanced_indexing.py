
def _has_advanced_indexing(index):
    """Check if there's any advanced indexing"""
    return any(
        isinstance(idx, (Sequence, bool))
        or (isinstance(idx, torch.Tensor) and (idx.dtype == torch.bool or idx.ndim > 0))
        for idx in index
    )

