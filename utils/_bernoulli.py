
def _bernoulli(key: Array, p: Array, shape: Shape | None, mode: str) -> Array:
  if shape is None:
    # TODO: Use the named part of `p` as well
    shape = np.shape(p)
  else:
    _check_shape("bernoulli", shape, np.shape(p))
  dtype = lax.dtype(p)

  if mode == 'high':
    u1, u2 = uniform(key, (2, *shape), dtype)
    # resolution of uniform samples is 2 ** -n_mantissa
    u2 *= 2 ** -dtypes.finfo(dtype).nmant
    return u2 < p - u1
  else:
    return uniform(key, shape, lax.dtype(p)) < p

