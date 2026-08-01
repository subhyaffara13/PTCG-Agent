
def _device_put_replicated(x, devices):
  mesh = jax.sharding.Mesh(
      np.array(devices), axis_names=('_device_put_replicated',)
  )
  sharding = jax.sharding.NamedSharding(
      mesh, jax.sharding.PartitionSpec('_device_put_replicated')
  )
  return jax.tree_util.tree_map(
      lambda v: jax.device_put(np.stack([v] * len(devices)), sharding), x
  )


def _device_put_replicated(x, devices):
  mesh = jax.sharding.Mesh(
      np.array(devices), axis_names=('_device_put_replicated',)
  )
  sharding = jax.sharding.NamedSharding(
      mesh, jax.sharding.PartitionSpec('_device_put_replicated')
  )
  return jax.tree_util.tree_map(
      lambda v: jax.device_put(np.stack([v] * len(devices)), sharding), x
  )

