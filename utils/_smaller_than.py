
def _smaller_than(shape: tuple[int, ...], min_shape: tuple[int, ...]) -> bool:
  """Returns True if one of the dim of `shape` is smaller than `min_shape`."""
  return any(dim < min_dim for dim, min_dim in zip(shape, min_shape))

