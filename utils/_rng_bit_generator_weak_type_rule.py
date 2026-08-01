
def _rng_bit_generator_weak_type_rule(key, *, shape, dtype, algorithm,
                                      out_sharding):
  del shape, dtype, algorithm
  return (key.weak_type, False)

