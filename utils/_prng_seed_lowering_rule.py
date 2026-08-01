
def _prng_seed_lowering_rule(ctx: LoweringRuleContext, *seeds):
  del ctx
  # In the KeyScalarBundle case we unpack the bundle and set the seed with
  # the list of scalars.
  if len(seeds) == 1 and isinstance(seeds[0], KeyScalarBundle):
    tpu.prng_set_seed_32(seeds[0].scalars)
    return []
  # For integer seeds, we can set the seed directly as PRNGSeed32Op natively
  # takes in a list of integers as input.
  all_integers = all(isinstance(seed.type, ir.IntegerType) for seed in seeds)
  if not all_integers:
    seed_types = [seed.type for seed in seeds]
    raise ValueError(f"All seed data must be scalar integers. Got {seed_types}")
  tpu.prng_set_seed_32(seeds)
  return []

