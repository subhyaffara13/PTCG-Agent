from typing import Any

def _execute_device_local_memory_transfer(
    *,
    token: jax.Array,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    src_allocation_key_as_array: jax.Array,
    src_transforms: tuple[Any, ...],
    dst_allocation_key_as_array: jax.Array,
    dst_transforms: tuple[Any, ...],
    barrier_allocation_key_as_array: jax.Array,
    source_info: source_info_util.SourceInfo | None = None,
):
  device_id_as_int = int(device_id)
  thread_id_as_int = int(thread_id)
  src_transforms = jax.tree.map(int, _remove_noop_transforms(src_transforms))
  dst_transforms = jax.tree.map(int, _remove_noop_transforms(dst_transforms))
  del device_id, thread_id

  transfer = DeviceLocalMemoryTransfer(
      device_id=device_id_as_int,
      grid_point_coords=grid_point_coords,
      thread_id=thread_id_as_int,
      src_allocation_key_as_array=src_allocation_key_as_array,
      src_transforms=src_transforms,
      dst_allocation_key_as_array=dst_allocation_key_as_array,
      dst_transforms=dst_transforms,
      barrier_allocation_key_as_array=barrier_allocation_key_as_array,
      source_info=source_info,
  )
  token = transfer.execute(token)
  return token

