
def call_make_allocation_request_array(
    *,
    token: jax.Array,
    memory_space_id: int,
    device_id: jax.Array,
    thread_id: jax.Array | None = None,
    initial_ref_count: int = 1,
) -> tuple[jax.Array, jax.Array]:
  return callback.io_callback(
      _make_allocation_request_array,
      (TOKEN_SHAPE_DTYPE, HostAllocationRequest.shape_and_dtype()),
      token=token,
      device_id=device_id,
      memory_space_id=memory_space_id,
      thread_id=thread_id,
      initial_ref_count=initial_ref_count,
      # The callback has no side-effect, so we allow this to be reordered
      # relative to other callbacks.
      ordered=False,
  )

