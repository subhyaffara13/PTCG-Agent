
def _sharding_num_replicas(
    sharding: jax.sharding.Sharding, global_shape: Shape
) -> int:
  """Get the number of unique replicas for a sharding/shape.

  Uses the devices_indices_map to get the mapping of devices to the slice of the
  global array. This gives us the domains of every shard, which may be
  non-unique. For any index (domain), we increment the count by one. When `n`
  devices have the same index, this results in the replica count for that index
  being `n`. We can assert that the number of replicas for each index should be
  the same.

  We can cache results because we typically expect `save` to be called
  repeatedly on the same model (with changing array values).
  The model shardings and shapes do not change during the course of a typical
  training run.

  Training typically occurs with stacked layers, so we expect the number of
  model parameters to be significantly less than the cache size. Checkpoints
  with unstacked layers may have thousands of parameters, but these are
  typically used for inference, so saving is less relevant.

  Args:
    sharding: Array sharding.
    global_shape: The global shape of the array.

  Returns:
    The number of unique replicas for the sharding/shape.
  """
  counts = collections.defaultdict(int)
  for index in sharding.devices_indices_map(global_shape).values():
    counts[numpy_utils.to_hashable_index(index, shape=global_shape)] += 1
  num_replicas = next(iter(counts.values()))
  assert all(count == num_replicas for count in counts.values())
  return num_replicas

