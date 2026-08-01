
def unreplicate(tree):
  """Returns a single instance of a replicated array."""
  def _unreplicate_one(x):
    # Avoid degraded performance under the new jax.pmap.
    # Handle 0-dimensional (scalar) arrays - cannot index into them
    if hasattr(x, 'ndim') and x.ndim == 0:
      return x
    if (
        not hasattr(x, 'sharding')
        or isinstance(x.sharding, jax.sharding.SingleDeviceSharding)
        or len(jax.local_devices()) == 1
    ):
      return x[0]
    if x.sharding.is_fully_replicated:
      return x.addressable_shards[0].data
    return x.addressable_shards[0].data.squeeze(0)

  return jax.tree_util.tree_map(_unreplicate_one, tree)

