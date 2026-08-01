
def make_sync_checkpointer(
    config: CheckpointerConfig = CheckpointerConfig(),
    rank_info: RankInfo | None = None,
    commit_hook: WriterHook | None = None,
) -> SyncCheckpointer:
    """
    Factory function to create a SyncCheckpointer instance with sensible defaults.

    This function creates a synchronous checkpointer with default components, automatically
    detecting rank information from the default process group if available, and using the
    provided component configurations.

    Args:
        config: CheckpointerConfig containing component-specific configurations
               (writer_config, staging_config, process_config). Defaults to CheckpointerConfig().
        rank_info: RankInfo for distributed training. Defaults to auto-detection from
                  the default PyTorch distributed process group if initialized, otherwise
                  falls back to single-rank (world_size=1, rank=0).
        commit_hook: Optional hook for custom actions before and after checkpoint commits.

    Returns:
        SyncCheckpointer: A configured synchronous checkpointer instance.

    Examples:
        # Simplest usage - auto-detect rank, default config
        checkpointer = make_sync_checkpointer()

        # Explicit rank configuration
        checkpointer = make_sync_checkpointer(
            rank_info=RankInfo(global_world_size=4, global_rank=0)
        )

        # Disable barrier
        from .barriers import BarrierConfig
        config = CheckpointerConfig(barrier_config=BarrierConfig(barrier_type=None))
        checkpointer = make_sync_checkpointer(config=config)
    """
    if rank_info is None:
        rank_info = _get_default_rank_info()

    reader = CheckpointReader(
        rank_info=rank_info,
    )

    barrier = create_barrier_from_config(config.barrier_config)

    writer = CheckpointWriter(
        config=config.writer_config,
        rank_info=rank_info,
        barrier=barrier,
        commit_hook=commit_hook,
    )

    return SyncCheckpointer(
        writer=writer,
        reader=reader,
    )

