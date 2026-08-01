
def is_empty_shape(s: core.Shape) -> bool:
  return any(d == 0 for d in s)


def is_empty_shape(s: Shape) -> bool:
  return any(definitely_equal(d, 0) for d in s)

