
def _persistent_checkpoint_handler(
    multiprocessing_options: checkpoint_manager.MultiprocessingOptions,
) -> PyTreeCheckpointHandler:
  """Create a PyTreeCheckpointHandler for local checkpoints."""
  # TODO(b/372291557) Selection of replica_id=0 could be problematic if we can't
  # guarantee that the primary slice (in which the primary process is present)
  # always has the shard with shard.replica_id=0 for all available arrays.
  registry = type_handler_registry.create_type_handler_registry(
      (
          jax.Array,
          type_handlers.ArrayHandler(
              primary_host=multiprocessing_options.primary_host,
              replica_id=0,
              use_replica_parallel=False,
          ),
      ),
  )
  return PyTreeCheckpointHandler(
      use_ocdbt=True,
      use_zarr3=True,
      multiprocessing_options=multiprocessing_options,
      type_handler_registry=registry,
  )

