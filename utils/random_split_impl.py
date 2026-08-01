
def random_split_impl(keys, *, shape):
  base_arr = random_split_impl_base(
      keys._impl, keys._base_array, keys.ndim, shape=shape)
  return PRNGKeyArray(keys._impl, base_arr)

