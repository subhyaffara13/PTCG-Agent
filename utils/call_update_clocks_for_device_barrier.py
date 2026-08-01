
def call_update_clocks_for_device_barrier(token, device_id: jax.Array):
  return callback.io_callback(
      _update_clocks_for_device_barrier,
      TOKEN_SHAPE_DTYPE,
      token,
      device_id,
  )

