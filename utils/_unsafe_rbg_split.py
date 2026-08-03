import math


def _unsafe_rbg_split(key: typing.Array, shape: prng.Shape) -> typing.Array:
  # treat 10 iterations of random bits as a 'hash function'
  num = math.prod(shape)
  _, keys = lax.rng_bit_generator(key, (10 * num, 4), dtype='uint32')
  return lax_slicing.slice_in_dim(
      keys, start_index=None, limit_index=None, stride=10).reshape(*shape, 4)

