
def _get_slice_shape(
    index: tuple[slice, ...], global_shape: tuple[int, ...]
) -> tuple[int, ...]:
  """Calculates the shape of a slice from a global shape, assuming step is always 1."""
  return tuple(
      s.indices(global_shape[i])[1] - s.indices(global_shape[i])[0]
      for i, s in enumerate(index)
  )

