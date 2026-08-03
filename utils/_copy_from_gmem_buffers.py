from typing import Any

def _copy_from_gmem_buffers(
    token,
    device_id: int,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    avals: Sequence[Any],
    gmem_buffer_keys: Sequence[jax.Array],
    target_buffer_keys: Sequence[jax.Array],
    transforms,
):
  for aval, gmem_buffer_key, target_buffer_key in zip(
      avals, gmem_buffer_keys, target_buffer_keys, strict=True
  ):
    if gpu_callbacks.is_gmem_memory_space(aval.memory_space):
      continue
    token = _load_and_store_between_allocation_keys(
        token=token,
        device_id=device_id,
        grid_point_coords=grid_point_coords,
        thread_id=thread_id,
        share_and_dtype=aval,
        load_allocation_key=gmem_buffer_key,
        store_allocation_key=target_buffer_key,
        transform=transforms,
    )
  return token

