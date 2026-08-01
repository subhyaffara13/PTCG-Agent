
def get_dummy_input_array(
    devices: Sequence[jax.Device],
) -> jax.Array:
  """Returns a dummy array with replicated sharding on the given devices."""
  mesh = jax.sharding.Mesh(np.array(devices), ('d',))
  sharding = jax.sharding.NamedSharding(mesh, jax.sharding.PartitionSpec())
  return jax.device_put(jnp.array(True, dtype=jnp.bool), sharding)

