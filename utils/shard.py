
def shard(xs):
  """Helper for pmap to shard a pytree of arrays by local_device_count.

  Args:
    xs: a pytree of arrays.
  Returns:
    A matching pytree with arrays' leading dimensions sharded by the
    local device count.
  """
  local_device_count = jax.local_device_count()
  return jax.tree_util.tree_map(
    lambda x: x.reshape((local_device_count, -1) + x.shape[1:]), xs
  )

