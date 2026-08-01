
def _compute_newshape(arr: Array, newshape: DimSize | Shape) -> Shape:
  """Fixes a -1 value in newshape, if present."""
  orig_newshape = newshape  # for error messages
  try:
    iter(newshape)  # pyrefly: ignore[no-matching-overload]
  except TypeError:
    newshape = [newshape]
  else:
    newshape: Sequence[DimSize]  # pyrefly: ignore[redefinition]
  newshape = core.canonicalize_shape(newshape)
  neg1s = [i for i, d in enumerate(newshape) if type(d) is int and d == -1]
  if len(neg1s) > 1:
    raise TypeError("can only specify one unknown axis size with a `-1` value, "
                    f"got {orig_newshape}")
  if neg1s:
    i, = neg1s
    other_sizes = (*newshape[:i], *newshape[i+1:])
    if (all(isinstance(d, int) for d in (*arr.shape, *other_sizes)) and
        arr.size % math.prod(other_sizes) != 0):
      raise TypeError(f"cannot reshape array of shape {arr.shape} (size {arr.size}) "
                      f"into shape {orig_newshape} because the product of "
                      f"specified axis sizes ({math.prod(other_sizes)}) does "
                      f"not evenly divide {arr.size}")
    sz = core.cancel_divide_tracers(arr.shape, other_sizes)
    if sz is not None:
      return (*newshape[:i], sz, *newshape[i+1:])
  else:
    if (all(isinstance(d, int) for d in (*arr.shape, *newshape)) and
        arr.size != math.prod(newshape)):
      raise TypeError(f"cannot reshape array of shape {arr.shape} (size {arr.size}) "
                      f"into shape {orig_newshape} (size {math.prod(newshape)})")
  return tuple(-core.divide_shape_sizes(arr.shape, newshape)
               if core.definitely_equal(d, -1) else d for d in newshape)

