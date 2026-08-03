from typing import Any

def _step_arr_on_state_devices(step: int, state: PyTree) -> jax.Array:
  """Creates a scalar step array on the same device list as `state`."""
  leaves = jax.tree.leaves(state)
  if not leaves:
    raise ValueError(
        'colocated save/restore requires a non-empty pytree of state or '
        'sharding leaves, but got an empty pytree.'
    )

  def _resolve_sharding(x: Any) -> jax.sharding.Sharding:
    if isinstance(x, jax.sharding.Sharding):
      return x
    if isinstance(x, jax.Array):
      return x.sharding
    raise TypeError(
        'colocated save/restore requires all pytree leaves to be jax.Array or '
        f'jax.sharding.Sharding. Found leaf type: {type(x).__name__}.'
    )

  shardings = [_resolve_sharding(x) for x in leaves]
  first_sharding = shardings[0]
  first_device_list_key = colocated_utils.device_list_signature(
      first_sharding
  )
  for sharding in shardings[1:]:
    if (
        colocated_utils.device_list_signature(sharding)
        != first_device_list_key
    ):
      raise ValueError(
          'colocated save/restore requires all pytree leaves to share the same '
          'device list.'
      )
  if isinstance(first_sharding, jax.sharding.NamedSharding):
    scalar_sharding = jax.sharding.NamedSharding(
        first_sharding.mesh, jax.sharding.PartitionSpec()
    )
  elif isinstance(first_sharding, jax.sharding.SingleDeviceSharding):
    scalar_sharding = first_sharding
  else:
    raise TypeError(
        'colocated save/restore requires NamedSharding or '
        'SingleDeviceSharding on state arrays, '
        f'but got {type(first_sharding).__name__}.'
    )
  return jax.device_put(jnp.array(step, dtype=jnp.int32), scalar_sharding)

