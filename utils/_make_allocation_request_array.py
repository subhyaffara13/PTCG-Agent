
def _make_allocation_request_array(
    *,
    token: jax.Array,
    memory_space_id: int,
    device_id: jax.Array,
    thread_id: jax.Array | None = None,
    initial_ref_count: int = 1,
) -> tuple[jax.Array, jax.Array]:
  device_id_as_int = int(device_id)
  thread_id_as_int = int(thread_id) if thread_id is not None else 0
  del device_id, thread_id

  return token, HostAllocationRequest(
      memory_space_id=memory_space_id,
      device_id=device_id_as_int,
      thread_id=thread_id_as_int,
      initial_ref_count=initial_ref_count,
  ).as_jax_array

