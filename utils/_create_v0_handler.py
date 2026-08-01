
def _create_v0_handler(
    context: context_lib.Context,
    *,
    type_handler_registry: v0_serialization_types.TypeHandlerRegistry,
    array_metadata_validator: array_metadata_store_lib.Validator = array_metadata_store_lib.Validator(),
) -> base_pytree_checkpoint_handler.BasePyTreeCheckpointHandler:
  """Creates a V0 handler from a V1 context."""
  return base_pytree_checkpoint_handler.BasePyTreeCheckpointHandler(
      save_concurrent_bytes=context.memory_options.write_concurrent_bytes,
      restore_concurrent_bytes=context.memory_options.read_concurrent_bytes,
      save_device_host_concurrent_bytes=context.memory_options.transfer_concurrent_bytes,
      use_ocdbt=context.array_options.saving.use_ocdbt,
      use_zarr3=context.array_options.saving.use_zarr3,
      use_compression=context.array_options.saving.use_compression,
      multiprocessing_options=v0_options_lib.MultiprocessingOptions(
          primary_host=context.multiprocessing_options.primary_host,
          active_processes=context.multiprocessing_options.active_processes,
          barrier_sync_key_prefix=context.multiprocessing_options.barrier_sync_key_prefix,
      ),
      type_handler_registry=type_handler_registry,
      enable_post_merge_validation=context.array_options.saving.enable_post_merge_validation,
      pytree_metadata_options=context.pytree_options.saving.pytree_metadata_options,
      array_metadata_validator=array_metadata_validator,
      enable_pinned_host_transfer=context.array_options.saving.enable_pinned_host_transfer,
      is_prioritized_key_fn=context.memory_options.is_prioritized_key_fn,
  )

