
def _roots_with_zeros(p: Array, num_leading_zeros: Array | int) -> Array:
  # Avoid lapack errors when p is all zero
  p = _where(len(p) == num_leading_zeros, 1.0, p)
  # Roll any leading zeros to the end & compute the roots
  roots = _roots_no_zeros(roll(p, -num_leading_zeros))
  # Sort zero roots to the end.
  roots = lax.sort_key_val(roots == 0, roots)[1]
  # Set roots associated with num_leading_zeros to NaN
  return _where(arange(roots.size) < roots.size - num_leading_zeros, roots, complex(np.nan, np.nan))

