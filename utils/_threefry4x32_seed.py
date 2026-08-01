
def _threefry4x32_seed(seed: typing.Array) -> typing.Array:
  """Create a single Threefry 4x32 PRNG key from an integer seed."""
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
  # Hash through threefry4x32 to fill all 4 words from the 2-word seed.
  out = threefry4x32_p.bind(
      k0,
      k1,
      np.uint32(0),
      np.uint32(0),
      np.uint32(0),
      np.uint32(0),
      np.uint32(0),
      np.uint32(0),
  )
  return jnp.stack([lax.expand_dims(x, [0]) for x in out], axis=0).reshape(4)

