
def _rng_bit_generator_shape_rule(key, *, shape, dtype, algorithm, out_sharding):
  del dtype, algorithm
  return (key.shape, tuple(shape))

