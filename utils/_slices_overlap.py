
def _slices_overlap(slice_or_idx1: slice | int, slice_or_idx2: slice | int):
  if isinstance(slice_or_idx1, int):
    slice_or_idx1 = slice(slice_or_idx1, slice_or_idx1 + 1)
  if isinstance(slice_or_idx2, int):
    slice_or_idx2 = slice(slice_or_idx2, slice_or_idx2 + 1)

  if slice_or_idx1 == slice(None):
    return _is_empty_slice(slice_or_idx2)
  if slice_or_idx2 == slice(None):
    return _is_empty_slice(slice_or_idx1)

  # TODO(jburnim): Handle non-zero steps.
  assert (slice_or_idx1.step == 1) or (slice_or_idx1.step is None)
  assert (slice_or_idx2.step == 1) or (slice_or_idx2.step is None)

  assert slice_or_idx1.start is not None
  assert slice_or_idx1.stop is not None
  assert slice_or_idx2.start is not None
  assert slice_or_idx2.stop is not None

  # NOTE: We are only comparing slices with known stops (and sizes).
  # Do we need to handle zero-length slices?
  return (slice_or_idx1.start <= slice_or_idx2.start < slice_or_idx1.stop) | (
      slice_or_idx2.start <= slice_or_idx1.start < slice_or_idx2.stop
  )

