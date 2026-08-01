
def _compute_squeeze_shape(shape, dimensions):
  dims_set = set(dimensions)
  if len(dims_set) != len(dimensions):
    raise ValueError(f"dimensions are not unique: {dimensions}")
  if not all(0 <= d < len(shape) for d in dims_set):
    raise ValueError(f"dimensions outside range [0, ndim): {dimensions}")
  if any(not core.definitely_equal(shape[d], 1) for d in dimensions):
    raise ValueError(
        "cannot select an axis to squeeze out which has size not equal to "
        f"one, got {shape=} and {dimensions=}")
  return tuple(s for i, s in enumerate(shape) if i not in dims_set)

