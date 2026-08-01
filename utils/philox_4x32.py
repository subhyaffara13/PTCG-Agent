
def philox_4x32(hi0, lo0, hi1, lo1, k_hi, k_lo, rounds = 10):
  """Philox 4x32 keyed hash function."""
  k_hi_const = jnp.array(K_HI_32, dtype=jnp.uint32)
  k_lo_const = jnp.array(K_LO_32, dtype=jnp.uint32)
  mul_a = jnp.array(MUL_A, dtype=jnp.uint32)
  mul_b = jnp.array(MUL_B, dtype=jnp.uint32)

  for i in range(rounds):
    # Compute the round.
    new_hi0, new_lo0 = mul32_hi_lo(mul_a, hi1)
    new_hi0 = new_hi0 ^ lo0 ^ k_hi
    new_hi1, new_lo1 = mul32_hi_lo(mul_b, hi0)
    new_hi1 = new_hi1 ^ lo1 ^ k_lo
    hi0, lo0, hi1, lo1 = new_hi0, new_lo0, new_hi1, new_lo1

    # Raise the key on all iterations except for the last round.
    if i != rounds - 1:
      k_hi = k_hi + k_hi_const
      k_lo = k_lo + k_lo_const
  return hi0, lo0, hi1, lo1

