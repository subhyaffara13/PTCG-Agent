
def normalize_slice(resolved_slice: Index, shape: Shape) -> Index:
  """Ensures that all slice start and stop values are positive.

  Precondition: it is assumed that the slice start and stop values for a
  dimension of length `dim` are already on the interval `[-dim, dim)`. In
  other words, no truncation would occur, so  the result of slicing an array
  of shape `shape` with the given slice would have the same shape as the
  apparent shape of the slice itself:
    `np.empty(shape)[resolve_slice].shape == slice_shape(resolved_slice)`

  Postcondition: the slice start and stop values for a dimension of length `dim`
  are on the interval `[0, dim)`.

  Args:
    resolved_slice: An N-dimensional slice with no `None` values.
    shape: An array shape.

  Returns:
    An equivalent N-dimensional slice, with no `None` values.
  """
  return tuple(
      slice(
          s.start if s.start >= 0 else dim + s.start,  # pytype:disable=unsupported-operands
          s.stop if s.stop >= 0 else dim + s.stop,  # pytype:disable=unsupported-operands
          s.step,
      )
      for s, dim in zip(resolved_slice, shape)
  )

