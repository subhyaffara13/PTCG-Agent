from typing import Any

def _load_and_store_between_allocation_keys(
    *,
    token: jax.Array,
    device_id: int,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    share_and_dtype: Any,
    load_allocation_key: jax.Array,
    store_allocation_key: jax.Array,
    transform,
):
  token, loaded_value = gpu_callbacks.call_get(
      token=token,
      result_shape_and_dtype=share_and_dtype,
      device_id=jnp.int32(device_id),
      grid_point_coords=grid_point_coords,
      thread_id=thread_id,
      allocation_key_as_array=load_allocation_key,
      transforms=transform,
  )
  token, _ = gpu_callbacks.call_swap(
      token=token,
      result_shape_and_dtype=share_and_dtype,
      device_id=jnp.int32(device_id),
      grid_point_coords=grid_point_coords,
      thread_id=thread_id,
      allocation_key_as_array=store_allocation_key,
      transforms=transform,
      val=loaded_value,
      mask=None,
  )
  return token

