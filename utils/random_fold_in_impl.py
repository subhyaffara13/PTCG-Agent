
def random_fold_in_impl(keys, msgs):
  base_arr = random_fold_in_impl_base(
      keys._impl, keys._base_array, msgs, keys.shape)
  return PRNGKeyArray(keys._impl, base_arr)

