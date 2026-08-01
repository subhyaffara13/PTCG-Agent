
def _dynamic_slice_indices(
    operand: Array | np.ndarray,
    start_indices: Array | np.ndarray | Sequence[ArrayLike],
    allow_negative_indices: bool | Sequence[bool],
  ) -> list[ArrayLike]:
  # Normalize the start_indices w.r.t. operand.shape
  if len(start_indices) != operand.ndim:
    msg = ("Length of slice indices must match number of operand dimensions ({} "
          "vs {})")
    raise ValueError(msg.format(len(start_indices), operand.shape))
  if not isinstance(start_indices, Sequence):
    if start_indices.ndim != 1:
      raise ValueError("Slice indices must be a 1D sequence, got {}"
                       .format(start_indices.shape))
    start_indices = list(start_indices)
  result: list[ArrayLike] = []
  if isinstance(allow_negative_indices, bool):
    allow_negative_indices = [allow_negative_indices] * len(start_indices)
  # Loop to correct for negative indices.
  for i, d, allow_negative_index in zip(
      start_indices, operand.shape, allow_negative_indices
  ):
    # If i is unsigned, then it cannot be negative.
    if dtypes.issubdtype(_dtype(i), np.unsignedinteger):
      result.append(i)
      continue
    # Test whether i and d are static to avoid unnecessary staging.
    if isinstance(i, (int, np.integer)) and core.is_constant_dim(d):
      if allow_negative_index:
        result.append(lax.convert_element_type(i + d if i < 0 else i, _dtype(i)))
      elif i < 0:
        raise ValueError(f"Index {i} is out of bounds for dimension {d} if "
                          "allow_negative_indices=False")
      else:
        result.append(lax.convert_element_type(i, _dtype(i)))
      continue
    d = core.dimension_as_value(d)
    if isinstance(i, (int, np.integer)):
      if allow_negative_index:
        result.append(i + lax.convert_element_type(d, _dtype(i)) if i < 0 else i)
      elif i < 0:
        raise ValueError(f"Index {i} is out of bounds for dimension {d} if "
                          "allow_negative_indices=False")
      else:
        result.append(i)
      continue
    if allow_negative_index:
      d_arr = lax.convert_element_type(d, _dtype(i))
      # pyrefly: ignore[unsupported-operation]
      result.append(lax.select(i < 0, i + d_arr, i))
    else:
      result.append(i)
  return result

