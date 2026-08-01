
def slice_count() -> int:
  """Returns the number of slices."""
  return (
      len(
          set(d.slice_index for d in jax.devices() if hasattr(d, 'slice_index'))
      )
      or 1
  )

