
def _get_warmup_ops(
    rank: int,
    n_local_stages: int,
    microbatches_per_round: int,
    pp_group_size: int,
    n_microbatches: int,
    multiply_factor: int = 2,
) -> int:
    """
    Calculate the number of warmup operations for interleaved schedules.
    """
    # Warmup operations for last stage
    warmups_ops_last_stage = (n_local_stages - 1) * microbatches_per_round
    # Increment warmup operations by multiply_factor for each hop away from the last stage
    warmup_ops = warmups_ops_last_stage + multiply_factor * ((pp_group_size - 1) - rank)
    # We cannot have more warmup operations than there are number of microbatches, so cap it there
    return min(warmup_ops, n_microbatches * n_local_stages)

