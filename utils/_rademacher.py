
def _rademacher(key, shape, dtype, out_sharding) -> Array:
  bernoulli_samples = bernoulli(key=key, p=0.5, shape=shape,
                                out_sharding=out_sharding).astype(dtype)
  return (2 * bernoulli_samples - 1).astype(dtype)

