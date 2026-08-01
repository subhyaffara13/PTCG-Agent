
def _check_shapes(shape_1, shape2):
    if shape_1 != shape2:
        raise AssertionError(f"shape mismatch: {shape_1} != {shape2}")


def _check_shapes(func_name, expected_name, actual, expected):
  actual_shapes = _map(np.shape, actual)
  expected_shapes = _map(np.shape, expected)
  if actual_shapes != expected_shapes:
    raise ValueError(
        f"{func_name}() output shapes must match {expected_name}, "
        f"got {actual_shapes} and {expected_shapes}")

