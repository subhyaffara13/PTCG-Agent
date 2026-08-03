from typing import Any, Callable

def _reduce_single_device_sharding(
    sharding: jax.sharding.SingleDeviceSharding,
) -> tuple[Callable[..., jax.sharding.SingleDeviceSharding], Any]:
  return _unreduce_single_device_sharding, (
      sharding.device_set.pop().id,
      sharding.memory_kind)

