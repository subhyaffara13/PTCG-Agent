import logging

def construct_maximal_shardings(
    abstract_state: PyTree, devices: Sequence[jax.Device] | None = None
) -> PyTree:
  """Construct a sharding that partitions each array as much as possible.

  This method is subject to change and should not be considered stable.

  Args:
    abstract_state: PyTree of jax.ShapeDtypeStruct.
    devices: Devices to shard across. If None, uses all available devices.

  Returns:
    PyTree of jax.sharding.Sharding.
  """
  shardings = jax.tree.map(
      lambda x: _construct_maximal_sharding(x, devices=devices), abstract_state
  )

  total_size = 0

  def _calculate_sharding_hbm_consumption(
      sds: jax.ShapeDtypeStruct, sharding: jax.sharding.Sharding
  ):
    nonlocal total_size
    shard_shape = sharding.shard_shape(sds.shape)
    total_size += np.prod(shard_shape) * sds.dtype.itemsize

  jax.tree.map(_calculate_sharding_hbm_consumption, abstract_state, shardings)
  logging.info('Expected per-device HBM consumption: %s', total_size)
  return shardings

