
def get_array_handler(
    context: context_lib.Context,
) -> type_handlers.ArrayHandler:
  """Returns the TypeHandler for JAX arrays (pytree leaves)."""
  saving_options = context.array_options.saving
  loading_options = context.array_options.loading
  primary_host = context.multiprocessing_options.primary_host
  common_kwargs = dict(
      primary_host=primary_host,
      replica_id=None if primary_host is None else 0,
      use_replica_parallel=saving_options.use_replica_parallel,
      min_slice_bytes_for_replica_parallel=saving_options.min_slice_bytes_for_replica_parallel,
      max_replicas_for_replica_parallel=saving_options.max_replicas_for_replica_parallel,
      enable_replica_parallel_separate_folder=saving_options.enable_replica_parallel_separate_folder,
      enable_write_sharding_file=saving_options.enable_write_sharding_file,
      array_metadata_store=saving_options.array_metadata_store,
  )
  if loading_options.use_load_and_broadcast:
    load_and_broadcast_kwargs = dict(
        replica_axis_index=loading_options.load_and_broadcast_options.replica_axis_index,
        primary_replica_id=loading_options.load_and_broadcast_options.primary_replica_id,
        broadcast_memory_limit_bytes=loading_options.load_and_broadcast_options.broadcast_memory_limit_bytes,
        broadcast_memory_scaling_factor=loading_options.load_and_broadcast_options.broadcast_memory_scaling_factor,
    )
  else:
    load_and_broadcast_kwargs = dict()

  if multihost.is_pathways_backend():
    checkpointing_impl = resolve_pathways_checkpointing_impl(context)
    return pathways_handler_registry.get_pathways_array_handler(
        use_single_replica_array_handler=loading_options.use_load_and_broadcast,
        checkpointing_impl=checkpointing_impl,
        **common_kwargs,
        **load_and_broadcast_kwargs,
    )
  else:
    if loading_options.use_load_and_broadcast:
      return jax_array_handlers.SingleReplicaArrayHandler(
          dispatcher=None,
          **common_kwargs,
          **load_and_broadcast_kwargs,
      )
    return jax_array_handlers.ArrayHandler(dispatcher=None, **common_kwargs)

