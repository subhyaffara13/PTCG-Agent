
def _normalize_index(index, axis_size):
  """Normalizes an index value in the range [-N, N) to the range [0, N)."""
  if dtypes.issubdtype(dtypes.dtype(index), np.unsignedinteger):
    return index
  if core.is_constant_dim(axis_size):
    axis_size_val = lax._const(index, axis_size)
  else:
    axis_size_val = lax.convert_element_type(core.dimension_as_value(axis_size),
                                             dtypes.dtype(index))
  if isinstance(index, (int, np.integer)):
    return lax.add(index, axis_size_val) if index < 0 else index
  else:
    return lax.select(index < 0, lax.add(index, axis_size_val), index)

