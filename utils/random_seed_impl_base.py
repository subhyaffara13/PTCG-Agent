
def random_seed_impl_base(seeds, *, impl):
  seed = iterated_vmap_unary(np.ndim(seeds), impl.seed)
  return seed(seeds)

