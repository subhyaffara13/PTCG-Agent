
def random_seed_impl(seeds, *, impl):
  base_arr = random_seed_impl_base(seeds, impl=impl)
  return PRNGKeyArray(impl, base_arr)

