
def _philox4x32_lowering(k0, k1, x0, x1, x2, x3):
  """Apply the Philox 4x32 hash with 10 rounds.

  Args:
    k0: uint32 array, the upper 32 bits of the 64-bit Philox key.
    k1: uint32 array, the lower 32 bits of the 64-bit Philox key.
    x0: uint32 array, the first word of the counter.
    x1: uint32 array, the second word of the counter.
    x2: uint32 array, the third word of the counter.
    x3: uint32 array, the fourth word of the counter.

  Returns:
    A tuple of four uint32 arrays (out0, out1, out2, out3).
  """
  for rnd in range(_DEFAULT_ROUNDS):
    # Bump key before each round except the first.
    if rnd > 0:
      k0 = k0 + _PHILOX_W32_0
      k1 = k1 + _PHILOX_W32_1

    # Philox round function:
    #   lo0, hi0 = mulhilo(M0, x0)
    #   lo1, hi1 = mulhilo(M1, x2)
    #   out = [hi1 ^ x1 ^ k0, lo1, hi0 ^ x3 ^ k1, lo0]
    lo0, hi0 = lax.mul(_PHILOX_M4x32_0, x0), lax.mulhi(_PHILOX_M4x32_0, x0)
    lo1, hi1 = lax.mul(_PHILOX_M4x32_1, x2), lax.mulhi(_PHILOX_M4x32_1, x2)

    x0_new = hi1 ^ x1 ^ k0
    x1_new = lo1
    x2_new = hi0 ^ x3 ^ k1
    x3_new = lo0

    x0, x1, x2, x3 = x0_new, x1_new, x2_new, x3_new

  return (x0, x1, x2, x3)

