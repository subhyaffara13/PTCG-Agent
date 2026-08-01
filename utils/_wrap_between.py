
def _wrap_between(x, _a):
  """Wraps `x` between `[-a, a]`."""
  a = lax._const(x, _a)
  two_a = lax._const(x, 2 * _a)
  zero = lax._const(x, 0)
  rem = lax.rem(lax.add(x, a), two_a)
  rem = lax.select(lax.lt(rem, zero), lax.add(rem, two_a), rem)
  return lax.sub(rem, a)

