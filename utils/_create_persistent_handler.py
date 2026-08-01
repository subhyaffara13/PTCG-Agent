
def _create_persistent_handler(
    mp_options: checkpoint_manager.MultiprocessingOptions,
    replica_axis_index: int,
    is_single_slice: bool,
) -> ocp.PyTreeCheckpointHandler:
  """Creates a PyTreeCheckpointHandler for persistent storage.

  Args:
    mp_options: Multiprocessing options for the checkpoint handler.
    replica_axis_index: The index of the replica axis in the mesh.
    is_single_slice: Whether the mesh is single-slice.

  Returns:
    A PyTreeCheckpointHandler configured for persistent storage.
  """
  handler = type_handlers.SingleReplicaArrayHandler(
      replica_axis_index=replica_axis_index,
      broadcast_memory_limit_bytes=1024 * 1024 * 1000,
      primary_host=mp_options.primary_host,
      replica_id=_PRIMARY_REPLICA_ID,
      use_replica_parallel=False,
  )
  if is_single_slice:
    handler = type_handlers.ArrayHandler(
        primary_host=mp_options.primary_host,
        replica_id=_PRIMARY_REPLICA_ID,
        use_replica_parallel=False,
    )
  registry = type_handler_registry.create_type_handler_registry(
      (
          jax.Array,
          handler,
      ),
  )
  return ocp.PyTreeCheckpointHandler(
      use_ocdbt=True,
      use_zarr3=True,
      multiprocessing_options=mp_options,
      type_handler_registry=registry,
  )

