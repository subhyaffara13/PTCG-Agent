
def _threefry_seed(seed: typing.Array) -> typing.Array:
  if seed.shape:
    raise TypeError(f"PRNG key seed must be a scalar; got {seed!r}.")
  if not np.issubdtype(seed.dtype, np.integer):
    raise TypeError(f"PRNG key seed must be an integer; got {seed!r}")
  convert = lambda k: lax.expand_dims(lax.convert_element_type(k, np.uint32), [0])
  k1 = convert(
      lax.shift_right_logical(seed, lax._const(seed, 32)))
  with config.numpy_dtype_promotion('standard'):
    # TODO(jakevdp): in X64 mode, this can generate 64-bit computations for 32-bit
    # inputs. We should avoid this.
    k2 = convert(jnp.bitwise_and(seed, np.uint32(0xFFFFFFFF)))
  return lax.concatenate([k1, k2], 0)

