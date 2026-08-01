
def _local_checkpoint_handler(
    multiprocessing_options: checkpoint_manager.MultiprocessingOptions,
) -> PyTreeCheckpointHandler:
  """Create a PyTreeCheckpointHandler for local checkpoints."""
  if multiprocessing_options.primary_host is not None:
    raise ValueError(
        'multiprocessing_options.primary_host must be set to None for local'
        ' checkpoints.'
    )
  local_registry = type_handler_registry.create_type_handler_registry(
      (
          jax.Array,
          type_handlers.ArrayHandler(
              primary_host=None,
              replica_id=None,
              use_replica_parallel=False,
          ),
      ),
  )
  return PyTreeCheckpointHandler(
      use_ocdbt=True,
      use_zarr3=True,
      multiprocessing_options=multiprocessing_options,
      type_handler_registry=local_registry,
  )


def _local_checkpoint_handler(
    multiprocessing_options: checkpoint_manager.MultiprocessingOptions,
    distributed_to_device_ids_fn: Callable[[], list[list[int]]] | None = None,
    save_concurrent_gb: int | None = None,
    restore_concurrent_gb: int | None = None,
) -> tuple[PyTreeCheckpointHandler, ProcessMetadataCheckpointHandler]:
  """Creates a PyTreeCheckpointHandler for local checkpoints.

  Args:
    multiprocessing_options: Options for distributed coordination.
    distributed_to_device_ids_fn: Function to dynamically fetch mapping of
      distributed indices to local device indices.
    save_concurrent_gb: Limit for save concurrency in GB.
    restore_concurrent_gb: Limit for restore concurrency in GB.

  Returns:
    A tuple of (PyTree checkpoint handler, process metadata handler).
  """
  if multiprocessing_options.primary_host is not None:
    raise ValueError(
        'multiprocessing_options.primary_host must be set to None for local'
        ' checkpoints.'
    )
  local_registry = type_handler_registry.create_type_handler_registry(
      (
          jax.Array,
          type_handlers.ArrayHandler(
              primary_host=None, replica_id=None, use_replica_parallel=False
          ),
      ),
  )
  pytree_handler = PyTreeCheckpointHandler(
      use_ocdbt=True,
      use_zarr3=True,
      multiprocessing_options=multiprocessing_options,
      type_handler_registry=local_registry,
      save_concurrent_gb=save_concurrent_gb,
      restore_concurrent_gb=restore_concurrent_gb,
  )
  metadata_handler = ProcessMetadataCheckpointHandler(
      multiprocessing_options=multiprocessing_options,
      distributed_to_device_ids_fn=distributed_to_device_ids_fn,
  )
  return pytree_handler, metadata_handler

