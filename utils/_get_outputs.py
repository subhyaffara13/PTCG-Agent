
def _get_outputs(
    token,
    device_id: int,
    output_buffers: Sequence[AllocationKeyAndValue],
) -> tuple[jax.Array, Sequence[Array]]:
  """Reads and returns values from the allocated output buffers."""
  outputs = []
  for buffer in output_buffers:
    token, val = gpu_callbacks.call_get(
        token=token,
        result_shape_and_dtype=buffer.value,
        device_id=jnp.int32(device_id),
        grid_point_coords=None,
        thread_id=jnp.int32(0),
        allocation_key_as_array=buffer.key,
        transforms=(),  # Read the entire buffer.
    )
    outputs.append(val)

  return token, outputs

