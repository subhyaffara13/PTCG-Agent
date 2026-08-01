
def worker_rank_array(worker_cpu_devices: Sequence[jax.Device]) -> jax.Array:
  """Builds a one-element-per-worker logical rank array."""
  if not worker_cpu_devices:
    raise ValueError('worker_cpu_devices must be non-empty.')
  mesh = jax.sharding.Mesh(np.asarray(worker_cpu_devices), (_WORKER_AXIS_NAME,))
  sharding = jax.sharding.NamedSharding(
      mesh, jax.sharding.PartitionSpec(_WORKER_AXIS_NAME)
  )
  worker_ranks = np.arange(len(worker_cpu_devices), dtype=np.int32)
  return jax.make_array_from_callback(
      worker_ranks.shape,
      sharding,
      lambda index: worker_ranks if index is None else worker_ranks[index],
      dtype=worker_ranks.dtype,
  )

