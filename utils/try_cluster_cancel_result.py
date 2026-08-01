
def TryClusterCancelResult(
    num_buffers: int | None = None) -> pallas_core.MemoryRef:
  """Helper function to create Refs for cluster launch control results.

  Args:
    num_buffers: Optional argument for specifying the number of buffers
      to allocate. If None, will return a single 16-byte buffer. If specified,
      will return a (num_buffers, 16)-shaped buffer.

  Returns:
    A MemoryRef with the correct shape for holding the opaque cluster launch
    control result.
  """
  if num_buffers is None:
    return SMEM((16,), jnp.int8)
  else:
    return SMEM((num_buffers, 16), jnp.int8)

