
def call_swap(
    *,
    token: jax.Array,
    result_shape_and_dtype,
    device_id: jax.Array,
    grid_point_coords: jax.Array,
    thread_id: jax.Array,
    allocation_key_as_array: jax.Array,
    transforms,
    val: jax.Array,
    mask: jax.Array | None,
    clock=None,
    source_info=None,
) -> tuple[jax.Array, jax.Array]:
  return callback.io_callback(
      functools.partial(_swap, source_info=source_info),
      (TOKEN_SHAPE_DTYPE, result_shape_and_dtype),
      token,
      device_id,
      grid_point_coords,
      thread_id,
      allocation_key_as_array,
      transforms,
      val,
      mask,
      clock=clock,
  )

