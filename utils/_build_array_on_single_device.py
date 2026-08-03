from typing import Any

def _build_array_on_single_device(
    info: dict[str, Any], owner: int, ctx: _LoadContext
) -> jax.Array:
  """Builds a global JAX array placed on a single device."""
  shape, dtype = _get_array_properties(info)
  target_device = ctx.devices_by_host[owner][0]
  single_device_sharding = jax.sharding.SingleDeviceSharding(target_device)

  if ctx.host_id == owner:
    if not ctx.bundle_bytes:
      np_array = np.zeros(shape, dtype=dtype)
    else:
      np_array = _extract_tensor_from_bundle(
          info, ctx.bundle_bytes, ctx.bundle_start_offset, shape, dtype
      )
    device_array = jax.device_put(np_array, target_device)
    device_buffers = [device_array]
  else:
    device_buffers = []

  return jax.make_array_from_single_device_arrays(
      shape, single_device_sharding, device_buffers, dtype=dtype
  )

