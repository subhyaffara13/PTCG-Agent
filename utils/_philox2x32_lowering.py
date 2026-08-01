
def _philox2x32_lowering(k0, x0, x1):
  """Apply the Philox 2x32 hash with 10 rounds.

  Args:
    k0: uint32 array, the Philox 2x32 key word.
    x0: uint32 array containing the upper 32 bits of the counter.
    x1: uint32 array containing the lower 32 bits of the counter.

  Returns:
    A tuple of two uint32 arrays (out0, out1).
  """
  for rnd in range(_DEFAULT_ROUNDS):
    # Bump key before each round except the first.
    if rnd > 0:
      k0 = k0 + _PHILOX_W32_0

    # Philox 2x32 round function:
    #   lo, hi = mulhilo(M2x32_0, x0)
    #   out = [hi ^ x1 ^ k0, lo]
    lo, hi = lax.mul(_PHILOX_M2x32_0, x0), lax.mulhi(_PHILOX_M2x32_0, x0)

    x0 = hi ^ x1 ^ k0
    x1 = lo

  return (x0, x1)

