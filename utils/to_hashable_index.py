
def to_hashable_index(
    idx: Index, *, shape: Shape | None = None
) -> HashableIndex:
  """Converts an Index into a hashable form.

  Optionally resolves the slices to a concrete index if the shape is provided.
  If not, conversion may fail if the slices are not concrete.

  Args:
    idx: The index to convert.
    shape: Global array shape.

  Returns:
    A hashable index.
  """
  idx = resolve_slice(idx, shape) if shape else idx

  return tuple([int_tuple_from_slice(s) for s in idx])

