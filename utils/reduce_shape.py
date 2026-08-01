
def reduce_shape(
    shape: Sequence[int], axes: Sequence[int], keep_dims: bool = False
) -> tuple[int, ...]:
  res = []
  for i, dim in enumerate(shape):
    if i in axes:
      if keep_dims:
        res.append(1)
    else:
      res.append(dim)
  return tuple(res)

