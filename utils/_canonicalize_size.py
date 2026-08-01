
def _canonicalize_size(size: int | Sequence[int] | None, *args: ArrayLike) -> tuple[int, ...]:
  if size is None:
    return np.broadcast_shapes(*(np.shape(arg) for arg in args))
  elif isinstance(size, (int, np.number)):
    return (operator.index(size),)
  else:
    return tuple(map(operator.index, size))

