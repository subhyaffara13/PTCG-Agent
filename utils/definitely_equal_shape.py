
def definitely_equal_shape(s1: Shape, s2: Shape) -> bool:
  """Check that two shapes are guaranteed to be element-wise equal.

  In presence of dynamic shapes may return False even when the shapes may
  be equal at runtime.
  """
  return (len(s1) == len(s2) and
          all(unsafe_map(definitely_equal, s1, s2)))

