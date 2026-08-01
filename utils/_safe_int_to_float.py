
def _safe_int_to_float(bits, dtype):
  """Converts bits: u32[2,...] into f32[...] in the range (0,1)."""
  if bits.dtype != np.uint32 or dtype != np.float32:
    raise RuntimeError("_safe_int_to_float only works for u32 -> f32")
  finfo = dtypes.finfo(dtype)
  hiclz, loclz = lax.clz(bits)
  hi, lo = bits

  mantissa = lax.bitwise_or(
      lax.shift_left(hi, hiclz),
      jnp.where(
          hiclz == 32,
          lax.shift_left(lo, loclz),
          lax.shift_right_logical(lo, finfo.bits - hiclz)))
  mantissa = lax.shift_right_logical(
      mantissa, np.array(finfo.bits - finfo.nmant - 1, dtype=np.uint32))
  mantissa = lax.bitwise_and(
      mantissa, np.array((1 << finfo.nmant) - 1, dtype=np.uint32))
  exp = lax.shift_left(
      (-finfo.minexp - jnp.where(hiclz == 32, 32 + loclz, hiclz)),
      np.array(finfo.nmant, dtype=np.uint32))
  exp = lax.bitwise_and(exp, np.array(
      (1 << (finfo.bits - 2)) - (1 << (finfo.nmant - 1)), dtype=np.uint32))
  return lax.bitwise_or(exp, mantissa).view(dtype)

