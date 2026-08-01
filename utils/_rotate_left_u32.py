
def _rotate_left_u32(x, d):
  """Rotate 32-bit unsigned integer x left by d bits."""
  d = np.uint32(d)
  return lax.shift_left(x, d) | lax.shift_right_logical(x, np.uint32(32) - d)

