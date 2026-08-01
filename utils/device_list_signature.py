
def device_list_signature(
    sharding: jax.sharding.Sharding,
) -> tuple[tuple[str, int], ...]:
  """Builds a stable device-list signature from public sharding APIs."""
  if isinstance(sharding, jax.sharding.NamedSharding):
    return tuple((d.platform, d.id) for d in sharding.mesh.devices.flat)
  if isinstance(sharding, jax.sharding.SingleDeviceSharding):
    d = next(iter(sharding.device_set))
    return ((d.platform, d.id),)
  return tuple(sorted((d.platform, d.id) for d in sharding.device_set))

