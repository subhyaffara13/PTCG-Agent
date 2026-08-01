
def seed_with_impl(impl: PRNGImpl, seed: int | typing.ArrayLike) -> PRNGKeyArray:
  return random_seed(seed, impl=impl)

