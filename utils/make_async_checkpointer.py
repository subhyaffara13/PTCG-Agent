
def make_async_checkpointer(
    config: CheckpointerConfig = CheckpointerConfig(),
    rank_info: RankInfo | None = None,
    subprocess_init_fn: Callable[..., None] = default_subprocess_init_fn,
    subprocess_init_args: tuple[Any, ...] = (),
    checkpoint_writer_init_fn: Callable[..., CheckpointWriter] = default_writer_init_fn,
    checkpoint_writer_init_args: dict[str, Any] | None = None,
) -> AsyncCheckpointer:
    """
    Factory function to create an AsyncCheckpointer instance with sensible defaults.

    This function creates an asynchronous checkpointer using the provided configuration,
    automatically detecting rank information if not provided.

    Args:
        config: CheckpointerConfig containing component-specific configurations.
        rank_info: RankInfo for distributed training. Defaults to auto-detection.
        subprocess_init_fn: Function to initialize the subprocess. Defaults to no-op.
        subprocess_init_args: Arguments to pass to subprocess_init_fn.
        checkpoint_writer_init_fn: Function to create CheckpointWriter instance.
        checkpoint_writer_init_args: Arguments to pass to checkpoint_writer_init_fn.

    Returns:
        AsyncCheckpointer: A configured asynchronous checkpointer instance.

    Examples:
        # Create with default config
        checkpointer = make_async_checkpointer()

        # Create with custom init functions
        checkpointer = make_async_checkpointer(
            subprocess_init_fn=my_subprocess_init_fn,
            checkpoint_writer_init_fn=my_writer_init_fn
        )
    """
    if rank_info is None:
        rank_info = _get_default_rank_info()

    reader = CheckpointReader(
        rank_info=rank_info,
    )

    checkpoint_stager = DefaultStager(
        config=config.staging_config,
    )

    checkpoint_writer_init_args = checkpoint_writer_init_args or {}

    checkpoint_process = CheckpointProcess(
        rank_info=rank_info,
        config=config.process_config,
        subprocess_init_fn=subprocess_init_fn,
        subprocess_init_args=subprocess_init_args,
        checkpoint_writer_init_fn=checkpoint_writer_init_fn,
        checkpoint_writer_init_args=checkpoint_writer_init_args,
    )

    return AsyncCheckpointer(
        checkpoint_stager=checkpoint_stager,
        checkpoint_process=checkpoint_process,
        reader=reader,
    )

