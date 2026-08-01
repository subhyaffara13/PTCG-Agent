
def _get_default_rank_info() -> RankInfo:
    """
    Get default rank information from the current distributed environment.

    Returns:
        RankInfo: Rank information from the default process group if initialized,
                 otherwise single-rank fallback.
    """
    if dist.is_initialized():
        return RankInfo(
            global_world_size=dist.get_world_size(),
            global_rank=dist.get_rank(),
        )
    else:
        # Single-rank fallback
        return RankInfo(global_world_size=1, global_rank=0)

