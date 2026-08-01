
def _update_instance_devices(
    uid: int, shardings: tuple[jax.sharding.Sharding, ...]
) -> None:
  """Caching version of _InstanceRegistry.update_devices()."""
  device_set = set()
  for sharding in shardings:
    device_set |= sharding.device_set
  SINGLETON_INSTANCE_REGISTRY.update_devices(uid, device_set)

