
def _gumbel(key, shape, dtype, mode) -> Array:
  _check_shape("gumbel", shape)
  info = dtypes.finfo(dtype)
  if dtype == np.float32 and mode == "highest":
    finfo = dtypes.finfo(dtype)
    bits = _random_bits(key, finfo.bits, shape=(2,) + shape)
    neg = lax.bitwise_not(bits)
    lo_bits = neg[1]
    # 1 - bits in u64 fixed point.
    neg = neg + jnp.array([
        lo_bits == np.array((1 << finfo.bits) - 1, dtype=np.uint32),
        jnp.ones_like(lo_bits)], dtype=np.uint32)
    flip_mask = bits[0] < np.array(1 << (finfo.bits - 1), dtype=np.uint32)
    x = _safe_int_to_float(jnp.where(flip_mask, bits, neg), dtype=np.float32)
    # use log1p for (0,0.5) and log for [0.5, 1).
    return jnp.where(flip_mask,
        -jnp.log(-jnp.log1p(-x)), -jnp.log(-jnp.log(x)))
  elif mode == "high" or mode == "highest":
    high, low = _uniform(key, minval=0., maxval=1.,
                         shape=(2,) + shape, dtype=dtype)
    # TODO(parkers): The condition is to protect against rounding up but
    # we should be able to add safely with the right addition operation.
    x = jnp.where(high >= 0.5, high,
        high + 2 ** -(info.nmant) * low + info.tiny)
    return -jnp.log(-jnp.log1p(-x))
  else:
    return -jnp.log(-jnp.log(
        _uniform(key, minval=info.tiny, maxval=1., shape=shape, dtype=dtype)))

