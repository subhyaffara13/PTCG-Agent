
def _allocate_buffers_for_inputs(
    token: jax.Array,
    device_id: int,
    invars: Sequence[Any],
    inputs: Sequence[jax.Array],
) -> tuple[jax.Array, list[jax.Array]]:
  """Allocates `GMEM` buffers for the `inputs` of a `pallas_call`."""
  # TODO(nrink): This code is a simplified version to the corresponding TPU
  # interpreter code. Eventually, we should merge the two.
  input_buffer_keys = []
  for var, value in safe_zip(invars, inputs):
    assert var.aval.dtype == value.dtype
    token, req = gpu_callbacks.call_make_allocation_request_array(
        token=token,
        device_id=jnp.int32(device_id),
        # All operands of a `pallas_call`/`core_map` that are arrays (i.e. that
        # are not sempahores, barriers etc.) are placed in `GMEM`. These arrays
        # (or slices thereof) may need to be copied into `SMEM` before executing
        # the kernel.
        memory_space_id=gpu_callbacks.get_memory_space_idx(
            mosaic_gpu_core.MemorySpace.GMEM
        ),
    )
    token, key = gpu_callbacks.call_allocate_buffer_for_all_threads(
        token, jnp.int32(device_id), None, req, value
    )
    input_buffer_keys.append(key)

  return token, input_buffer_keys

