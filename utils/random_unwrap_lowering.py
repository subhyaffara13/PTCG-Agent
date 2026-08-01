
def random_unwrap_lowering(ctx, keys):
  return [keys]


def random_unwrap_lowering(ctx: LoweringRuleContext, key):
  keys_aval = ctx.avals_in[0]
  assert isinstance(keys_aval.dtype, prng.KeyTy)
  impl = keys_aval.dtype._impl
  if not pl_random.is_pallas_impl(impl):
    return key
  raise ValueError(
      "key_data not support for Pallas PRNG keys. Use"
      " split_pallas_seed instead."
  )

