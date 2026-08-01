
def random_seed_abstract_eval(seeds_aval, *, impl):
  return keys_shaped_array(impl, seeds_aval.shape, seeds_aval.sharding,
                           seeds_aval.mat)

