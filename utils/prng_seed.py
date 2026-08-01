
def prng_seed(*seeds: int | jax.Array) -> None:
  """Sets the seed for PRNG.

  Args:
    seeds: One or more integer seeds for setting the PRNG seed. If
      more than one seed is passed in, the seed material will be
      mixed before setting the internal PRNG state.
  """
  prng_seed_p.bind(*seeds)

