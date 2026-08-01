
def _dilate(operand, factors, fill_value=0):
  # this logic is like lax.pad, but with two leading dimensions, no edge
  # padding, and factors are at least 1 (interior padding is at least 0)
  outspace = np.add(operand.shape[2:],
                     np.multiply(np.subtract(factors, 1),
                                  np.subtract(operand.shape[2:], 1)))
  out = np.full(operand.shape[:2] + tuple(outspace), fill_value, operand.dtype)
  lhs_slices = tuple(_slice(None, None, step) for step in factors)
  out[(_slice(None),) * 2 + lhs_slices] = operand
  return out

