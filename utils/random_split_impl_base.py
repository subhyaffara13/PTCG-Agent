
def random_split_impl_base(impl, base_arr, keys_ndim, *, shape):
  split = iterated_vmap_unary(keys_ndim, lambda k: impl.split(k, shape))
  return split(base_arr)

