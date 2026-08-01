
def random_bits_impl_base(impl, base_arr, keys_ndim, *, bit_width, shape):
  bits = iterated_vmap_unary(
      keys_ndim, lambda k: impl.random_bits(k, bit_width, shape))
  return bits(base_arr)

