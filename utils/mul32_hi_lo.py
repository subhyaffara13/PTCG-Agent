
def mul32_hi_lo(x: jax.Array, y: jax.Array) -> tuple[jax.Array, jax.Array]:
  """Multiplies 2 32-bit values and returns the hi+low bits of the result."""
  xhi = x >> 16
  yhi = y >> 16
  xlo = x & 0xffff
  ylo = y & 0xffff

  xy_hi = xhi * yhi
  xy_lo = xlo * ylo
  cross_xy = xhi * ylo
  cross_yx = xlo * yhi
  carry = (cross_xy & 0xffff) + (cross_yx & 0xffff) + (xy_lo >> 16)
  result_hi = xy_hi + (cross_xy >> 16) + (cross_yx >> 16) + (carry >> 16)
  result_lo = (carry << 16) + (xy_lo & 0xffff)
  return result_hi, result_lo

