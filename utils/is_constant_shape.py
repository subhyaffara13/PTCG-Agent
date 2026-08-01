
def is_constant_shape(s: Shape) -> bool:
  # Whether the shape is a static constant.
  return all(is_constant_dim(d) for d in s)

