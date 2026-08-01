
def _try_broadcast_shapes(*shapes: tuple[int, ...], name: str) -> tuple[int, ...]:
  """
  Attempt to broadcast shapes, raising a TypeError if broadcasting fails.
  """
  if not shapes:
    raise TypeError(f"{name}: At least one shape is required.")
  ranks = {len(shape) for shape in shapes}
  if len(ranks) != 1:
    raise TypeError(f'{name}: arrays must have the same number of dimensions,'
                    f' got {ranks}')
  result_shape = []
  for ds in zip(*shapes):
    if all(core.same_referent(d, ds[0]) for d in ds[1:]):
      # if all axes are identical objects, the resulting size is the object
      result_shape.append(ds[0])
    else:
      # if all dims are equal (or 1), the result is the non-1 size
      non_1s = [d for d in ds if not core.definitely_equal(d, 1)]
      if not non_1s:
        result_shape.append(1)
      elif all(core.definitely_equal(non_1s[0], d) for d in non_1s[1:]):
        result_shape.append(non_1s[0])
      else:
        raise TypeError(f'{name} got incompatible shapes for broadcasting: '
                        f'{", ".join(map(str, map(tuple, shapes)))}.')
  return tuple(result_shape)

