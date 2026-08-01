
def _parse_indices(
    indices: tuple[Index, ...],
    shape: tuple[int, ...],
) -> list[ParsedIndex]:
  """Parse indices in the context of an array shape.

  Args:
    indices: a tuple of user-supplied indices to be parsed.
    shape: the shape of the array being indexed.

  Returns:
    The list of parsed indices stored in :class:`ParsedIndex` objects.
    This list will have the same length as ``indices``.

  Raises:
    IndexError: if any unrecognized index types are present or if there
      are too many indices, or too many ellipses.
  """
  # 1. go through indices to count the number of consumed dimensions.
  # This is required to determine the effect of any ellipses.
  dimensions_consumed: list[int] = []
  ellipses_indices: list[int] = []
  index_types: list[IndexType] = []
  for i, idx in enumerate(indices):
    typ = IndexType.from_index(idx)
    index_types.append(typ)

    if typ == IndexType.NONE:
      dimensions_consumed.append(0)
    elif typ == IndexType.ELLIPSIS:
      # We don't yet know how many dimensions are consumed, so set to zero
      # for now and update later.
      dimensions_consumed.append(0)
      ellipses_indices.append(i)
    elif typ == IndexType.BOOLEAN:
      dimensions_consumed.append(np.ndim(idx))  # pyrefly: ignore[bad-argument-type]
    elif typ in [IndexType.INTEGER, IndexType.ARRAY, IndexType.SLICE, IndexType.DYNAMIC_SLICE]:
      dimensions_consumed.append(1)
    else:
      raise IndexError(f"Unrecognized index type: {typ}")

  # 2. Validate the consumed dimensions and ellipses.
  if len(ellipses_indices) > 1:
    raise IndexError("an index can only have a single ellipsis ('...')")
  total_consumed = sum(dimensions_consumed)
  if total_consumed > len(shape):
    raise IndexError(f"Too many indices: array is {len(shape)}-dimensional,"
                     f" but {total_consumed} were indexed")
  if ellipses_indices:
    dimensions_consumed[ellipses_indices[0]] = len(shape) - total_consumed

  # 3. Generate the final sequence of parsed indices.
  result: list[ParsedIndex] = []
  current_dim = 0
  for index, typ, n_consumed in safe_zip(indices, index_types, dimensions_consumed):
    consumed_axes = tuple(range(current_dim, current_dim + n_consumed))
    current_dim += len(consumed_axes)
    result.append(ParsedIndex(index=index, typ=typ, consumed_axes=consumed_axes))
  return result

