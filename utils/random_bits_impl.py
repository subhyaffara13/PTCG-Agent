
def random_bits_impl(keys, *, bit_width, shape):
  return random_bits_impl_base(keys._impl, keys._base_array, keys.ndim,
                               bit_width=bit_width, shape=shape)

