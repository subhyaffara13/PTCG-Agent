
def _bfloat16_nulp_diff(x: np.ndarray, y: np.ndarray) -> np.ndarray:
  """Number of representable bf16 points between each item in x and y."""
  rx = x.view(np.int16)
  ry = y.view(np.int16)
  # The constant for two's complement adjustment, same as for float16.
  comp = np.int16(-(2**15))
  # Transform the integer representations of negative numbers, to make the
  # integer representation monotonic across the full range of floats.
  rx = np.where(rx < 0, comp - rx, rx)
  ry = np.where(ry < 0, comp - ry, ry)
  diff = np.abs(rx.astype(np.int32) - ry.astype(np.int32))
  return diff.astype(np.float64)

