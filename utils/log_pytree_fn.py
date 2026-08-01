
def log_pytree_fn(inp: Any, metadata: dict[str, Any]):
  """Logs information about the input pytree and metadata.

  Args:
    inp: The input pytree of jax.Arrays.
    metadata: Additional metadata to log.
  """

  def _log_fn(arr: jax.Array):
    sharding = arr.sharding
    assert isinstance(sharding, jax.sharding.NamedSharding)

    pytree_utils.log_pytree('array_in_worker', arr)
    mesh_utils.pretty_log_mesh('array mesh in worker: ', sharding.mesh)
    logging.info(
        'process=%s/%s, addressable_shards=%s, mesh_devices=%s',
        multihost.process_index(),
        multihost.process_count(),
        arr.addressable_shards,
        sharding.mesh.devices,
    )

  logging.info('metadata: %s', metadata)
  logging.info(
      'metadata sharding mesh devices in worker: %s',
      metadata['array_sharding'].mesh.devices,
  )
  jax.tree.map(_log_fn, inp)

