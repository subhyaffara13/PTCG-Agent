
def default_writer_init_fn(rank_info: RankInfo) -> CheckpointWriter:
    """Default checkpoint writer initialization function."""
    return CheckpointWriter(
        config=CheckpointWriterConfig(),
        rank_info=rank_info,
    )

