
def _get_checkpoint_manager_options(
    options: ReplicatorCheckpointManagerOptions,
    multiprocessing_options: checkpoint_manager.MultiprocessingOptions,
) -> checkpoint_manager.CheckpointManagerOptions:
  """Get options for checkpoint manager."""
  per_process_directory_creation = multiprocessing_options.primary_host is None
  return checkpoint_manager.CheckpointManagerOptions(
      save_interval_steps=options.save_interval_steps,
      step_name_format=options.step_name_format,
      should_save_fn=options.should_save_fn,
      multiprocessing_options=multiprocessing_options,
      create=True,
      cleanup_tmp_directories=False,  # Handled separately below.
      enable_background_delete=True,
      enable_async_checkpointing=options.enable_async_checkpointing,
      preservation_policy=options.preservation_policy,
      enable_per_process_directory_creation=per_process_directory_creation,
  )

