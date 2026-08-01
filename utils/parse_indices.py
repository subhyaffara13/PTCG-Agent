
def parse_indices(
    index, shape: Sequence[int], *, check_oob: bool = True
) -> tuple[list[ir.Value | int], list[int], list[bool]]:
  if not isinstance(index, tuple):
    index = (index,)
  if trailing_dims := len(shape) - len(index):
    index += (slice(None),) * trailing_dims
  base_indices = []
  slice_shape = []
  is_squeezed = []
  for axis, (idx, bound) in enumerate(zip(index, shape)):
    if isinstance(idx, (ir.Operation, ir.OpView)):
      idx = idx.result
    if isinstance(idx, int):
      if check_oob and (idx >= bound or (idx < 0 and -idx > bound)):
        raise IndexError(
            f"Index {idx} along axis {axis} is out of bounds for shape {shape}"
        )
      base_indices.append(idx if idx >= 0 else bound + idx)
      slice_shape.append(1)
      is_squeezed.append(True)
    elif isinstance(idx, slice):
      if idx.step is not None and idx.step != 1:
        raise NotImplementedError("Strided slices not implemented")
      start = idx.start or 0
      if start < 0:
        start = bound + start
      stop = idx.stop or bound
      if stop < 0:
        stop = bound + stop
      if check_oob and (
          start < 0 or start >= bound or stop < 0 or stop > bound
      ):
        raise IndexError(
            f"Slice {idx} along axis {axis} is out of bounds for shape {shape}"
        )
      base_indices.append(start)
      slice_shape.append(stop - start)
      is_squeezed.append(False)
    elif isinstance(idx, DynamicSlice):
      if check_oob and (
          isinstance(idx.base, int) and idx.base + idx.length > bound
      ):
        raise IndexError(
            f"Slice {idx} along axis {axis} is out of bounds for shape {shape}"
        )
      base_indices.append(idx.base)
      slice_shape.append(idx.length)
      is_squeezed.append(False)
    elif isinstance(idx, ir.Value):
      if not isinstance(idx.type, ir.IndexType):
        raise ValueError("Expected an index-typed index")
      base_indices.append(idx)
      slice_shape.append(1)
      is_squeezed.append(True)
    else:
      raise NotImplementedError(type(idx))
  assert len(base_indices) == len(slice_shape) == len(is_squeezed) == len(shape)
  return base_indices, slice_shape, is_squeezed

