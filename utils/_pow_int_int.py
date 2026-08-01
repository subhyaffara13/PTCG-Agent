
def _pow_int_int(x1, x2):
  # Integer power => use binary exponentiation.
  bits = 6  # Anything more would overflow for any x1 > 1
  zero = _constant_like(x2, 0)
  one = _constant_like(x2, 1)
  # Initialize acc carefully such that pow(0, x2) is zero for x2 != 0
  acc = _where(lax.bitwise_and(lax.eq(x1, zero), lax.ne(x2, zero)), zero, one)
  for _ in range(bits):
    acc = _where(lax.bitwise_and(x2, one), lax.mul(acc, x1), acc)
    x1 = lax.mul(x1, x1)
    x2 = lax.shift_right_logical(x2, one)
  return acc

