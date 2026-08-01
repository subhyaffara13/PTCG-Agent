
def _validate_shape_and_dtype_for_per_device_arrays(
    arrays: Sequence[ArrayImpl | np.ndarray | literals.TypedNdArray],
    sharding: Sharding,
    aval: core.ShapedArray,
    expected_shape: Shape,
):
  """Validates that per-device arrays are valid and consistent."""
  expected_dtype = aval.dtype
  for db in arrays:
    if db.dtype != expected_dtype:
      raise ValueError(
          "Input buffers to `Array` must have matching dtypes. "
          f"Got {db.dtype}, expected {expected_dtype} for buffer: {db}"
      )
    if db.shape != expected_shape:
      raise ValueError(
          f"Expected shard shape {expected_shape} doesn't match the single "
          f"device array shape {db.shape}. Shape of Array is "
          f"{aval.str_short()} with sharding {sharding}"
      )

