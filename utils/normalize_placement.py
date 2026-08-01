
def normalize_placement(p: Placement, tensor_shape: tuple[int, ...]) -> Placement:
    """
    Normalize a placement for a given tensor shape.

    Converts Shard on a size-1 dimension to Replicate for deduplication.
    Shard(0) on a [1, 4] tensor puts all data on rank 0 and an empty [0, 4]
    on rank 1. Rank 1's empty computation is vacuous (contributes nothing
    after redistribution), so the validation outcome is determined entirely
    by rank 0, which has the full data — same as Replicate. We gain no
    signal from testing S(0) on a size-1 dim beyond what R already provides,
    so we normalize to R to avoid spurious "missing rule" noise when ground
    truth and DTensor use different forms for size-1 dims.
    """
    if is_trivial_shard(p, tensor_shape):
        return Replicate()
    return p

