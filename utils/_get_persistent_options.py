
def _get_persistent_options(
    options: CheckpointManagerOptions,
    multiprocessing_options: checkpoint_manager.MultiprocessingOptions,
) -> checkpoint_manager.CheckpointManagerOptions:
  """Get options for persistent checkpoint manager."""
  return checkpoint_manager.CheckpointManagerOptions(
      save_interval_steps=options.persistent.save_interval_steps,
      max_to_keep=options.persistent.max_to_keep,
      keep_period=options.persistent.keep_period,
      step_name_format=options.step_name_format,
      create=False,
      cleanup_tmp_directories=options.cleanup_tmp_directories,
      async_options=options.async_options,
      multiprocessing_options=multiprocessing_options,
      enable_async_checkpointing=options.enable_async_checkpointing,
      should_save_fn=options.persistent.should_save_fn,
      save_root_metadata=False,
      save_decision_policy=options.persistent.save_decision_policy,
      preservation_policy=options.persistent.preservation_policy,
  )

