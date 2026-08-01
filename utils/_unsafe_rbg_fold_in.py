
def _unsafe_rbg_fold_in(key: typing.Array, data: typing.Array) -> typing.Array:
  assert not data.shape
  _, random_bits = lax.rng_bit_generator(_rbg_seed(data), (10, 4), dtype='uint32')
  return key ^ random_bits[-1]

