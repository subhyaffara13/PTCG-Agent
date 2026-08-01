
def _num_slices() -> int:
  """Returns number of slices."""
  if hasattr(jax.devices()[0], 'slice_index'):
    return max(d.slice_index for d in jax.devices()) + 1
  return 1

