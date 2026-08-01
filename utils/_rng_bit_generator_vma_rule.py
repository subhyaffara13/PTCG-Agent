
def _rng_bit_generator_vma_rule(key, *, shape, dtype, algorithm, out_sharding):
  return (key.mat.varying, frozenset())

