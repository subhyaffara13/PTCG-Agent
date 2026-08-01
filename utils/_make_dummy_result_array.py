
def _make_dummy_result_array(
    pytree: PyTree, abstract: bool = False
) -> jax.Array | jax.ShapeDtypeStruct:
  """Returns a dummy array with replicated across the devices in the pytree.

  Args:
    pytree: The pytree to use to determine the devices.
    abstract: Whether to return a jax.ShapeDtypeStruct instead of a jax.Array.

  Returns:
    A dummy array with replicated sharding across the devices in the pytree.
    If abstract is True, returns a jax.ShapeDtypeStruct instead.
  """
  devices = set()
  jax.tree.map(lambda x: devices.update(x.sharding.device_set), pytree)
  device_list: list[jax.Device] = sorted(list(devices), key=lambda d: d.id)
  replicated_sharding = jax.sharding.NamedSharding(
      jax.sharding.Mesh(device_list, ('d',)),
      jax.sharding.PartitionSpec(),
  )
  if abstract:
    return jax.ShapeDtypeStruct((), jnp.bool, sharding=replicated_sharding)
  else:
    return jax.make_array_from_callback(
        (), replicated_sharding, lambda _: True, dtype=jnp.bool
    )

