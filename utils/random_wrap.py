
def random_wrap(base_arr, *, impl):
  _check_prng_key_data(impl, base_arr)
  return random_wrap_p.bind(base_arr, impl=impl)

