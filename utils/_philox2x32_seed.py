
def _philox2x32_seed(seed: typing.Array) -> typing.Array:
  """Internal implementation of philox2x32_seed."""
  if seed.shape:
    raise TypeError(f"PRNG key seed must be a scalar; got {seed!r}.")
  if not np.issubdtype(seed.dtype, np.integer):
    raise TypeError(f"PRNG key seed must be an integer; got {seed!r}")
  convert = lambda k: lax.convert_element_type(k, np.uint32)
  k0 = convert(
      lax.shift_right_logical(seed, lax.convert_element_type(32, seed.dtype))
  )
  with config.numpy_dtype_promotion("standard"):
    k1 = convert(jnp.bitwise_and(seed, np.uint32(0xFFFFFFFF)))
  # Hash through philox2x32 to mix the seed bits into a 1-word key.
  # Use both seed halves as counter words so they both influence the output.
  out0, _ = philox2x32_p.bind(np.uint32(0), k0, k1)
  return jnp.array([out0], dtype=np.uint32)

