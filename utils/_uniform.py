
def _uniform(key, minval, maxval, shape, dtype) -> Array:
  _check_shape("uniform", shape)
  if not dtypes.issubdtype(dtype, np.floating):
    raise TypeError("uniform only accepts floating point dtypes.")

  minval = lax.convert_element_type(minval, dtype)
  maxval = lax.convert_element_type(maxval, dtype)
  minval = lax.broadcast_to_rank(minval, len(shape))
  maxval = lax.broadcast_to_rank(maxval, len(shape))

  finfo = dtypes.finfo(dtype)
  nbits, nmant = finfo.bits, finfo.nmant

  if nbits not in (8, 16, 32, 64):
    raise TypeError(
        f"uniform only accepts 8-, 16-, 32-, or 64-bit dtypesgot {dtype}."
    )

  rng_bits = nbits
  if nmant < 8:
    rng_bits = 8
  bits = _random_bits(key, rng_bits, shape)
  uint_dtype = UINT_DTYPES[nbits]
  if rng_bits != nbits:
    bits = lax.convert_element_type(bits, uint_dtype)

  # The strategy here is to randomize only the mantissa bits with an exponent of
  # 1 (after applying the bias), then shift and scale to the desired range. The
  # bit-level transformation we use relies on Numpy and XLA having bit-for-bit
  # equivalent float representations, which might not be true on all platforms.
  float_bits = lax.shift_right_logical(
      bits, jnp.array(rng_bits - nmant, uint_dtype))
  float_bits = lax.bitwise_or(
      float_bits,
      # The double cast is because the TPU backend does not implement `view` on
      # float64 values => do the `view` in NumPy first, but then ensure that
      # we have a JAX array that won't be canonicalized further.
      jnp.asarray(np.array(1.0, dtype).view(float_bits.dtype),
                  dtype=float_bits.dtype))
  floats = lax.bitcast_convert_type(float_bits, dtype) - jnp.array(1., dtype)
  return lax.max(
      minval,
      lax.reshape(floats * (maxval - minval) + minval, shape))

